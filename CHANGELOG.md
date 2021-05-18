# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.5.0] - 2021-05-17
### Added
- Add `only_commit_author` parameter.

## [0.4.0] - 2021-05-12
### Added
- Add `pre_release` parameter.

## [0.3.0] - 2021-05-11
### Added
- Add `version_file_path` parameter.
- Add `user_name` parameter.
- Add `user_email` parameter.

### Changed
- Commit and push changelog and version files.

## [0.2.0] - 2021-04-23
### Added
- Add `github_token` parameter.

### Removed
- Remove credentials and response content from logs in case of failure.

## [0.1.0] - 2021-04-23
### Changed
- Log all available credentials and response content in case of failure.

## [0.0.4] - 2021-04-23
### Fixed
- Do not prefix GitHub URL by `$` anymore.

## [0.0.3] - 2021-04-23
### Fixed
- Handle the fact that `WORKDIR` changes when using as a drone plugin.

## [0.0.2] - 2021-04-22
### Fixed
- Include python script in Docker image.

## [0.0.1] - 2021-04-21
### Added
- Initial release.

[Unreleased]: https://github.com/ets-infra/drone-github-release/compare/0.5.0...master
[0.5.0]: https://github.com/ets-infra/drone-github-release/compare/0.4.0...0.5.0
[0.4.0]: https://github.com/ets-infra/drone-github-release/compare/0.3.0...0.4.0
[0.3.0]: https://github.com/ets-infra/drone-github-release/compare/0.2.0...0.3.0
[0.2.0]: https://github.com/ets-infra/drone-github-release/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/ets-infra/drone-github-release/compare/0.0.4...0.1.0
[0.0.4]: https://github.com/ets-infra/drone-github-release/compare/0.0.3...0.0.4
[0.0.3]: https://github.com/ets-infra/drone-github-release/compare/0.0.2...0.0.3
[0.0.2]: https://github.com/ets-infra/drone-github-release/compare/0.0.1...0.0.2
[0.0.1]: https://github.com/ets-infra/drone-github-release/releases/tag/0.0.1
