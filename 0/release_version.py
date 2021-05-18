import os

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

    def post(self, uri: str, content: dict) -> requests.Response:
        response = self.client.post(
            url=f"{self.base_url}{uri}",
            json=content
        )
        if not response:
            raise Exception(f"Unable to POST to {response.url}: {response.text} (HTTP {response.status_code})")
        response.raise_for_status()
        return response

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
    if (only_author := os.getenv('PLUGIN_ONLY_COMMIT_AUTHOR')) and (only_author != os.getenv("DRONE_COMMIT_AUTHOR")):
        print(f"Skipping GitHub release creation as commit author ({os.getenv('DRONE_COMMIT_AUTHOR')}) is not {only_author}.")
        return

    release = get_latest_version()

    github = GitHub()

    github.add_release(
        tag=release["version"],
        branch=os.getenv("DRONE_TARGET_BRANCH"),
        title=f"{release['version']} ({release['release_date']})",
        content=release["raw"],
        pre_release=os.getenv('PLUGIN_PRE_RELEASE') is not None
    )


def get_latest_version() -> dict:
    changelog_path = os.getenv('PLUGIN_CHANGELOG_PATH', "CHANGELOG.md")
    releases = keepachangelog.to_raw_dict(changelog_path)
    new_version = sorted(releases.keys())[-1]
    return releases[new_version]


if __name__ == "__main__":
    create_github_release()
