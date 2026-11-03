# Changelog

All notable chatrdc changes are documented here. The project has not declared a production release.

## [Unreleased]

### Added

- Local FastAPI agent with read-only health and bounded system-summary endpoints.
- Loopback-only launcher and a local status dashboard.
- Stdio MCP connector exposing read-only health and system-summary tools.
- Host/Origin validation for browser-facing local requests.
- Loopback validation for the MCP agent URL.
- Unit tests for agent endpoints, host/origin protections, and MCP URL validation.
- Repository baseline validator now skips generated/dependency/cache directories (`.venv`, `build`, `dist`, etc.) to avoid false-positive broken-link reports in local environments; unit tests added.
- PHASE 0 repository state report and PHASE 1 findings register under `docs/engineering/`.

### Changed

- Initialized README and ABOUT for the chatrdc product.
- Replaced generic Makefile placeholders with project lint, test, build, security, and CI commands.
- Extended CI and CodeQL configuration for the Python application while retaining repository-baseline validation.
- CI lint/format scope now includes `scripts/validate_repo.py` and `tests/test_validate_repo.py`.

### Security

- Kept LAN and Internet ingress disabled by default.
- Explicitly documented that device enrollment, authenticated remote access, desktop-control capabilities, signed installers, and verified ChatGPT integration are not yet implemented.
