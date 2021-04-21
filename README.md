# Create GitHub release based on changelog

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
