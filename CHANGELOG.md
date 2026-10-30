# Changelog

All notable chatrdc changes are documented here. The project has not declared a production release.

## [Unreleased]

### Added

- Local FastAPI agent with read-only health and bounded system-summary endpoints.
- Loopback-only launcher and a local status dashboard.
- Stdio MCP connector exposing read-only health and system-summary tools.
- Host/Origin validation for browser-facing local requests.
- Baseline response security headers and regression coverage for accepted and rejected requests.
- Loopback validation for the MCP agent URL.
- Unit tests for agent endpoints, bounded error responses, Host/Origin edge cases, response headers, and MCP URL validation.
- Product-specific architecture, development, startup, security, release, and readiness documentation.

### Changed

- Initialized README and ABOUT for the chatrdc product.
- Replaced generic Makefile placeholders with project lint, test, build, security, and CI commands.
- Extended CI and CodeQL configuration for the Python application while retaining repository-baseline validation.

### Security

- Kept LAN and Internet ingress disabled by default.
- Explicitly documented that device enrollment, authenticated remote access, desktop-control capabilities, signed installers, and verified ChatGPT integration are not yet implemented.
