# Security Policy

## Reporting a vulnerability

Do not disclose exploitable vulnerabilities in public issues, pull requests, discussions, commit messages, logs, or generated evidence bundles. Use [GitHub private vulnerability reporting](https://github.com/cvsz/chatrdc/security) when available.

## Supported versions

No production release has been declared. Until a release policy is published, treat the default branch and feature branches as development software only.

## Current security boundary

The initial implementation is a local-only, read-only diagnostic scaffold:

- Bind the agent to `127.0.0.1` only and disable forwarded-proxy header trust when no trusted reverse proxy is configured.
- The MCP server communicates with the local agent over loopback.
- The agent rejects non-loopback Host values and mismatched browser Origin values.
- Agent responses disable caching and set anti-sniffing, anti-framing, referrer, and restrictive browser feature-policy headers.
- Expose only health and bounded host-summary data.
- Return generic diagnostic errors without exposing internal exception details.
- Do not expose arbitrary shell, file writes, process termination, service control, screen capture, or remote desktop control.
- Do not place credentials, private keys, device secrets, or personal data in the repository.
- Never put a production endpoint or secret in an example configuration.

## Mandatory gates before LAN or Internet remote access

1. Cryptographically random, revocable per-device credentials and explicit device enrollment.
2. Authenticated operator identity and device-scoped authorization, including deny-by-default behavior.
3. TLS through a supported gateway/tunnel; never expose the agent port directly.
4. Browser Host/Origin and CSRF protections for any browser-facing state-changing operation.
5. Explicit approval gates for sensitive operations and a strict capability allowlist.
6. Append-only audit events with secret/PII redaction and defined retention.
7. Rate limits, bounded request sizes, timeouts, replay protections, and safe reconnect behavior.
8. Dependency/SAST/secret scanning, SBOM, reproducible builds, signed installers, and credential/key rotation.
9. Threat model, abuse-case tests, Windows/Linux/WSL2 integration tests, and independent security review.
10. Verified rollback, incident response, and operator ownership.

## Engineering expectations

Treat model output, repository content, remote requests, and generated artifacts as untrusted data. Model intent is a request, not authorization. Future write/execute operations must use explicit allowlisted capabilities, canonical path validation, least privilege, and per-operation consent.

A green CI run or the presence of a security control in documentation is not evidence that it is effective. Report only directly verified results.
