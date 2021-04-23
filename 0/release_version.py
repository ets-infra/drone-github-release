import os

import keepachangelog
import requests


def create_github_release(release: dict):
    # Base GitHub URL
    github_link = os.getenv("DRONE_REPO_LINK")[:-len(os.getenv("DRONE_REPO"))]
    # Name of the repository on GitHub. Usually organization/repository or user/repository
    github_repository_name = os.getenv("DRONE_REPO")
    # GitHub token used to create the release
    github_token = os.getenv('PLUGIN_GITHUB_TOKEN', os.getenv("DRONE_GIT_PASSWORD"))
    if not github_token:
        raise Exception("github_token parameter must be provided as DRONE_GIT_PASSWORD environment variable is not set.")
    # GitHub target release branch name
    github_branch = os.getenv("DRONE_TARGET_BRANCH")

    response = requests.post(
        url=f"{github_link}api/v3/repos/{github_repository_name}/releases",
        headers={'Authorization': f"token {github_token}"},
        json={
            "tag_name": release["version"],
            "target_commitish": github_branch,
            "name": f"{release['version']} ({release['release_date']})",
            "body": release["raw"],
            "draft": False,
            "prerelease": False
        }
    )
    response.raise_for_status()


def add_version_tag():
    changelog_path = os.getenv('PLUGIN_CHANGELOG_PATH', "CHANGELOG.md")
    releases = keepachangelog.to_raw_dict(changelog_path)
    new_version = sorted(releases.keys())[-1]
    create_github_release(releases[new_version])


if __name__ == "__main__":
    add_version_tag()
