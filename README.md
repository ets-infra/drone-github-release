# Supported tags and respective Dockerfile links

- [`1.0.1`, `latest`](https://github.com/ets-infra/drone-github-release/blob/master/1/Dockerfile)

# Quick reference (cont.)

- **Where to file issues**: [https://github.com/ets-infra/drone-github-release/issues](https://github.com/ets-infra/drone-github-release/issues)

# What is the purpose of this image?

[Drone](https://www.drone.io) plugin to create a GitHub release based on changelog following [keepachangelog](https://keepachangelog.com/en/1.1.0/) format.

<p align="center">
    <a href="https://www.drone.io"><img alt="drone logo" src="https://raw.githubusercontent.com/drone/brand/master/logos/png/dark/drone-logo-png-dark-128.png"></a>
</p>

The following steps are executed by this plugin:

1. Gather the latest version number based on changelog.
2. Create a GitHub release for this version and with the content described by the changelog.

| Parameter | Description |
|:---|---|
| changelog_path | Path to the changelog. Default to `CHANGELOG.md` in current folder. |
| github_token | Token (repo permission) used to create the release. Default to [the drone GIT password](https://docs.drone.io/server/reference/drone-git-password/) (if available). Related user needs to have admin role in repository. |
| pre_release | If provided (value does not matter), this will be a GitHub pre-release. |
| only_commit_author | If provided and the value does not matches the one from [the commit author user name](https://docs.drone.io/pipeline/environment/reference/drone-commit-author/), this plugin will not do anything. |

# How to use this image

## Add a step to your drone pipeline

```yaml
kind: pipeline
type: docker
name: default

steps:
- name: tag
  image: etsinfra/drone-github-release:latest
  settings:
    changelog_path: custom_folder/CHANGELOG.md
    github_token: cc1cc11111111ccc1c11c1cc1ccc1c1cc1111c1c
```
