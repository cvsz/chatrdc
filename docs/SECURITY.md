# Security model and release gates

The canonical policy is [SECURITY.md](../SECURITY.md). This document summarizes implementation-level constraints.

## Current boundary

- Agent launch binds to `127.0.0.1:8765`.
- Host validation allows loopback hostnames only.
- Browser Origin, when supplied, must match the request's loopback host and port.
- MCP connector accepts a loopback-only HTTP URL.
- Read-only diagnostics only; no generic shell or file-write tools.
- Bounded HTTP response reads and short request timeout in MCP bridge.
- Generic API errors rather than stack traces.
- No environment variables, process command lines, or user document contents in the API response.

## Required before remote access

1. Cryptographically random, revocable per-device credentials and enrollment.
2. User sessions and device-scoped authorization.
3. TLS and a supported gateway/tunnel; never expose the agent port directly.
4. CSRF/origin/host protections for browser-facing endpoints.
5. Approval gates for writes, command execution, process/service control, and screen sharing.
6. Append-only audit events with secret/PII redaction.
7. Rate limits, request limits, timeouts, replay protections, safe reconnect.
8. Dependency scanning, SBOM, signed installers, and key rotation.
9. Independent review and Windows/Linux/WSL2 E2E acceptance.

Treat model intent as a request, not authorization. Future write/execute operations must use explicit allowlisted capabilities, canonical path validation, least privilege, and per-operation consent.
