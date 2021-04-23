import netrc
import os
from typing import Dict

import keepachangelog
import requests
import requests.exceptions


def get_netrc_content() -> Dict[str, tuple]:
    try:
        return netrc.netrc().hosts
    except:
        return {}


def create_github_release(release: dict):
    # Base GitHub URL
    github_link = os.getenv("DRONE_REPO_LINK")[:-len(os.getenv("DRONE_REPO"))]
    # Name of the repository on GitHub. Usually organization/repository or user/repository
    github_repository_name = os.getenv("DRONE_REPO")
    # GitHub token used to create the release
    github_token = os.getenv("DRONE_GIT_PASSWORD")
    # GitHub target release branch name
    github_branch = os.getenv("DRONE_TARGET_BRANCH")
    netrc_content = get_netrc_content()

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
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise Exception(f"{github_token=}\n{netrc_content=}\n{e}: {response.text}")


def add_version_tag():
    changelog_path = os.getenv('PLUGIN_CHANGELOG_PATH', "CHANGELOG.md")
    releases = keepachangelog.to_raw_dict(changelog_path)
    new_version = sorted(releases.keys())[-1]
    create_github_release(releases[new_version])


if __name__ == "__main__":
    add_version_tag()
