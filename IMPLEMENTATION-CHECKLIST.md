# chatrdc Implementation Checklist

Use this checklist to track actual project delivery. Check items only when direct evidence exists for the exact scope; a planned change or green generic CI does not establish production readiness.

## Project initialization

- [x] Product identity documented in README.md and ABOUT.md on the feature branch.
- [x] CODEOWNERS retains the existing repository owner rather than inventing a team.
- [x] Security reporting link points to cvsz/chatrdc.
- [ ] Confirm identity changes through PR review and merge.
- [ ] Run and record the repository validator against the exact PR head.
- [ ] Verify effective repository administration controls by provider read-back.

## Local foundation

- [x] Python package/runtime declared in pyproject.toml.
- [x] Local agent exposes read-only health and bounded system summary.
- [x] Agent launch path binds to loopback by default.
- [x] Host and browser Origin checks added to the local agent.
- [x] Baseline no-store, anti-framing, anti-sniffing, referrer, and Permissions Policy response headers added.
- [x] MCP stdio server exposes read-only health and system-summary tools.
- [x] MCP target URL is restricted to loopback.
- [x] Local status dashboard added.
- [x] Python CI validation configured for Linux and Windows runners.
- [x] Regression tests cover malformed/mismatched Origin values, generic error responses, and response security headers.
- [ ] Execute full lint/test/build/security suite on the exact PR head.
- [ ] Verify fresh-clone installation on Windows 11.
- [ ] Verify fresh-clone installation on Linux and WSL2.
- [ ] Add MCP host/client integration acceptance evidence.

## Identity and remote access — release blockers

- [ ] Threat model and abuse cases reviewed independently.
- [ ] Operator authentication implemented and tested.
- [ ] Per-device enrollment, cryptographically random credentials, revocation, and rotation implemented.
- [ ] Device-scoped authorization and deny-by-default policy implemented.
- [ ] Secure TLS gateway/tunnel design reviewed; no direct agent ingress.
- [ ] Request signing/replay protections, rate limits, timeouts, and bounded request sizes implemented.
- [ ] Browser Host/Origin and CSRF protections verified for every state-changing route.
- [ ] Append-only audit events, redaction, and retention policy implemented.
- [ ] Remote-access negative/abuse tests pass.
- [ ] Independent security review approves the exact commit.

## Desktop capabilities — not currently implemented

- [ ] Define individually allowlisted capabilities and permission model.
- [ ] Require explicit consent/approval for sensitive actions.
- [ ] Add platform-specific Windows and Linux/WSL2 adapters.
- [ ] Do not add arbitrary shell execution or unrestricted file/process/service control.
- [ ] Add UI confirmation, audit, cancellation, and recovery behavior for every state-changing action.

## Packaging and operations

- [ ] Reproducible Windows and Linux/WSL2 packaging.
- [ ] Signed installers and artifact provenance/attestation.
- [ ] Upgrade, uninstall, key revocation, and rollback tests.
- [ ] Structured logs and appropriate health/readiness/alerting.
- [ ] Incident-response ownership and escalation documented.
- [ ] Dependency/SAST/secret scanning and SBOM evidence reviewed.
- [ ] Load/capacity testing where applicable.
- [ ] Verify all applicable release gates; document justified NOT APPLICABLE items.

## Final rule

Do not claim LAN/Internet remote access, real desktop control, deployment, signed installers, verified ChatGPT integration, or production readiness until the corresponding gates above have direct evidence.
