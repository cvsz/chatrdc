# About chatrdc

Remote Desktop Commander is a security-first desktop management foundation for Windows and Linux/WSL2.

## Product definition

- **Problem:** provide a governed foundation for managing and observing authorized desktop devices through a local agent and MCP connector.
- **Initial users:** authorized operators and developers managing their own or explicitly enrolled devices.
- **Initial scope:** read-only local health and system summary, MCP diagnostics, and a local status UI.
- **Explicit non-goals for the first increment:** arbitrary command execution, remote shell, file mutation, process/service control, screen capture, unattended remote control, public ingress, and production deployment.
- **Connectivity:** loopback only until authenticated device enrollment and secure gateway controls are implemented and verified.
- **Platforms:** Windows and Linux/WSL2 are the target matrix; support claims require per-platform test evidence.
- **Success measures:** deterministic tests, least-privilege interfaces, auditable authorization, secure defaults, and reproducible installation.

## Maintainer and ownership

- Repository owner: [cvsz](https://github.com/cvsz)
- Technical ownership and release approval: repository CODEOWNERS and GitHub rulesets; verify effective settings before release.

## Readiness

This repository is under active implementation. Scaffold tests do not establish production readiness, secure remote access, or verified ChatGPT integration.
