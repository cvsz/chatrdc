# chatrdc Roadmap

The roadmap is evidence-driven. A checked implementation item means code/docs exist; it does not mean the item is deployed or production-ready.

## P0 — Local foundation

- [x] Product identity and scope documented.
- [x] Read-only local agent health and system summary.
- [x] Loopback-only launch path.
- [x] Local dashboard.
- [x] Read-only MCP stdio tools.
- [x] Host/Origin validation and loopback-only MCP target validation.
- [x] Unit tests for local endpoints and configuration validation.
- [ ] Verify lint, tests, build, dependency audit, and repository baseline on exact PR head.
- [ ] Verify Windows 11, Linux, and WSL2 installation/behavior.
- [ ] Verify MCP host integration end-to-end.

## P1 — Identity and secure remote connectivity

- [ ] Threat model and abuse-case specification.
- [ ] Operator authentication and device enrollment.
- [ ] Revocable, rotated per-device credentials.
- [ ] Device-scoped authorization and deny-by-default policy.
- [ ] Secure TLS gateway/tunnel with no direct agent ingress.
- [ ] Rate limits, replay protection, bounded requests, audit and revocation.
- [ ] Independent security review and negative testing.

## P2 — Desktop management capabilities

- [ ] Define a strict allowlisted capability model.
- [ ] Implement consent/approval and auditable action lifecycle.
- [ ] Build Windows adapter and tests.
- [ ] Build Linux/WSL2 adapter and tests.
- [ ] Add safe, cancellable desktop operations only after authorization gates pass.
- [ ] Cross-platform integration and recovery testing.

## P2 — Packaging and operations

- [ ] Reproducible installer/build workflows.
- [ ] Signed artifacts, provenance and SBOM.
- [ ] Upgrade/uninstall/rollback and credential revocation verification.
- [ ] Structured logs, health/readiness, alerting and incident response.
- [ ] Verified release workflow and environment-specific acceptance.

## P3 — ChatGPT/client integration

- [ ] Identify supported ChatGPT MCP/connector configuration for the target account/product.
- [ ] Register the connector using documented configuration.
- [ ] Verify a real end-to-end tool invocation and permission boundary.
- [ ] Document version/limitations only after verification.

## Non-goals until security gates pass

- Arbitrary shell execution.
- Unrestricted file/process/service control.
- Unattended remote control or screen capture.
- Publicly exposing the local agent port.
- Claims of deployment or production readiness without evidence.
