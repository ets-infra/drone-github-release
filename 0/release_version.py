import os
from typing import Iterable

import keepachangelog
import requests


class GitHub:
    def __init__(self):
        token = os.getenv('PLUGIN_GITHUB_TOKEN', os.getenv("DRONE_GIT_PASSWORD"))
        if not token:
            raise Exception("github_token parameter must be provided as DRONE_GIT_PASSWORD environment variable is not set.")

        github_link = os.getenv("DRONE_REPO_LINK")[:-len(os.getenv("DRONE_REPO"))]
        self.base_url = f"{github_link}api/v3/repos/{os.getenv('DRONE_REPO')}"
        self.client = requests.Session()
        self.client.headers = {'Authorization': f"token {token}", "Accept": "application/vnd.github.v3+json"}

    def get(self, uri: str) -> requests.Response:
        response = self.client.get(
            url=f"{self.base_url}{uri}",
        )
        response.raise_for_status()
        return response

    def post(self, uri: str, content: dict) -> requests.Response:
        response = self.client.post(
            url=f"{self.base_url}{uri}",
            json=content
        )
        if not response:
            raise Exception(f"Unable to POST to {response.url}: {response.text} (HTTP {response.status_code})")
        response.raise_for_status()
        return response

    def put(self, uri: str, content: dict) -> requests.Response:
        response = self.client.put(
            url=f"{self.base_url}{uri}",
            json=content
        )
        if not response:
            raise Exception(f"Unable to PUT to {response.url}: {response.text} (HTTP {response.status_code})")
        response.raise_for_status()
        return response

    def get_last_commit(self, branch: str) -> str:
        return self.get(f"/branches/{branch}").json()['commit']['sha']

    def commit(self, file_path: str) -> str:
        with open(file_path) as file:
            content = file.read()
        return self.post(
            "/git/blobs",
            {
                "content": content,
                "encoding": "utf-8"
            }
        ).json()['sha']

    def push_files(self, last_commit_sha: str, *file_paths: str) -> str:
        return self.post(
            "/git/trees",
            {
                "base_tree": last_commit_sha,
                "tree": [
                    {
                        "path": file_path,
                        "mode": "100644",
                        "type": "blob",
                        "sha": self.commit(file_path)
                    }
                    for file_path in file_paths
                ]
            }
        ).json()['sha']

    def update_last_commit(self, branch: str, new_commit: str):
        self.post(
            f"/git/refs/heads/{branch}",
            {
                "ref": f"refs/heads/{branch}",
                "sha": new_commit
            }
        )

    def commit_and_push(self, user_name: str, user_email: str, branch: str, message: str, file_paths: Iterable[str]):
        previous_protection = self.disable_protection(branch)
        try:
            last_commit_sha = self.get_last_commit(branch)
            tree_sha = self.push_files(last_commit_sha, *file_paths)
            new_commit = self.post(
                "/git/commits",
                {
                    "message": message,
                    "author": {
                        "name": user_name,
                        "email": user_email
                    },
                    "parents": [
                        last_commit_sha
                    ],
                    "tree": tree_sha
                }
            ).json()['sha']
            self.update_last_commit(branch, new_commit)
        finally:
            self.set_protection(branch, previous_protection)

    def get_protection(self, branch: str) -> dict:
        return self.get(
            f"/branches/{branch}/protection",
        ).json()

    def set_protection(self, branch: str, protection: dict) -> dict:
        required_pull_request_reviews = {
            "dismissal_restrictions": {
                "users": dismissal_restrictions["users"],
                "teams": [team["slug"] for team in dismissal_restrictions["teams"]],
            } if (dismissal_restrictions := required_pull_request_reviews["dismissal_restrictions"]) else None,
            "dismiss_stale_reviews": required_pull_request_reviews["dismiss_stale_reviews"],
            "require_code_owner_reviews": required_pull_request_reviews["require_code_owner_reviews"],
        } if (required_pull_request_reviews := protection["required_pull_request_reviews"]) else None
        restrictions = {
            "users": restrictions["users"],
            "teams": [team["slug"] for team in restrictions["teams"]],
            "apps": restrictions["apps"],
        } if (restrictions := protection["restrictions"]) else None
        return self.put(
            f"/branches/{branch}/protection",
            content={
                "required_status_checks": protection["required_status_checks"],
                "enforce_admins": (protection["enforce_admins"] or {}).get("enabled"),
                "required_pull_request_reviews": required_pull_request_reviews,
                "restrictions": restrictions,
                "required_linear_history": (protection["required_linear_history"] or {}).get("enabled"),
                "allow_force_pushes": (protection["allow_force_pushes"] or {}).get("enabled"),
                "allow_deletions": (protection["allow_deletions"] or {}).get("enabled"),
            }
        ).json()

    def disable_protection(self, branch: str) -> dict:
        previous_protection = self.get_protection("master")
        self.set_protection(branch, {
            "required_status_checks": None,
            "enforce_admins": previous_protection["enforce_admins"],
            "required_pull_request_reviews": None,
            "restrictions": previous_protection["restrictions"],
            "required_linear_history": previous_protection["required_linear_history"],
            "allow_force_pushes": previous_protection["allow_force_pushes"],
            "allow_deletions": previous_protection["allow_deletions"],
        })
        return previous_protection

    def add_release(self, tag: str, branch: str, title: str, content: str, pre_release: bool):
        self.post(
            "/releases",
            {
                "tag_name": tag,
                "target_commitish": branch,
                "name": title,
                "body": content,
                "draft": False,
                "prerelease": pre_release
            }
        )


def create_github_release():
    files_to_commit = []

    changelog_path = os.getenv('PLUGIN_CHANGELOG_PATH', "CHANGELOG.md")
    files_to_commit.append(changelog_path)

    version_file_path = os.getenv('PLUGIN_VERSION_FILE_PATH')
    if version_file_path:
        files_to_commit.append(version_file_path)

    release = get_latest_version(changelog_path)

    github = GitHub()

    github.commit_and_push(
        user_name=os.getenv('PLUGIN_USER_NAME', os.getenv("DRONE_COMMIT_AUTHOR_NAME")),
        user_email=os.getenv('PLUGIN_USER_EMAIL', os.getenv("DRONE_COMMIT_AUTHOR_EMAIL")),
        branch=os.getenv("DRONE_TARGET_BRANCH"),
        message=f"Release {release['version']}",
        file_paths=files_to_commit
    )

    github.add_release(
        tag=release["version"],
        branch=os.getenv("DRONE_TARGET_BRANCH"),
        title=f"{release['version']} ({release['release_date']})",
        content=release["raw"],
        pre_release=os.getenv('PLUGIN_PRE_RELEASE') is not None
    )


def get_latest_version(changelog_path: str) -> dict:
    releases = keepachangelog.to_raw_dict(changelog_path)
    new_version = sorted(releases.keys())[-1]
    return releases[new_version]


if __name__ == "__main__":
    create_github_release()
