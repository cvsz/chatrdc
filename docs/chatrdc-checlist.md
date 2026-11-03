# CHAT RDC — ENTERPRISE PRODUCTION IMPLEMENTATION CHECKLIST

**Project:** ZEAZDEV ChatRDC  
**Repository:** https://github.com/cvsz/chatrdc  
**Target:** Enterprise Production-Grade Final Release  
**Execution Model:** Security-First / Evidence-Driven / Incremental Delivery  
**Independent Reviewer:** `policedbc`  
**Authorized Merge Identity:** `cvsz`

---

## 0. EXECUTION CONTROL

### 0.1 Project Governance

- [x] Confirm repository URL and ownership. — https://github.com/cvsz/chatrdc, owner cvsz (git remote + GitHub API, VERIFIED)
- [x] Identify current default branch. — `main` (GitHub API, VERIFIED)
- [x] Identify current development branch. — `staging/connectivity-first` (git branch, VERIFIED)
- [x] Record exact HEAD SHA. — `f19e339627c16254d4aa2e6f94899287f22600b7` (git log, VERIFIED)
- [x] Inspect Git working tree. — clean except untracked `docs/checlist.md`, `docs/ent-pro-e2e-master-prompt.md`, `package-lock.json` (git status, VERIFIED)
- [x] Identify all linked worktrees. — `/home/cvsz/chatrdc` (healthy), `/home/cvsz/chatrdc-validator` c356049 detached (healthy), `/home/cvsz/chatrdc-connectivity-signed` BROKEN gitdir (F2, BLOCKED, preserved) (git worktree list, VERIFIED)
- [x] Identify uncommitted modifications. — none (working tree clean after commit f19e339) (git status, VERIFIED)
- [x] Identify untracked files. — `docs/checlist.md`, `docs/ent-pro-e2e-master-prompt.md`, `package-lock.json` (git status, VERIFIED; preserved, not committed)
- [ ] Verify local backups. — no dedicated backup worktree found; `chatrdc-local-backup-20261104-013529` not present on disk (UNVERIFIED)
- [x] Read all applicable `AGENTS.md`. — repository AGENTS.md read (VERIFIED)
- [x] Review repository governance requirements. — GOVERNANCE.md, CONTRIBUTING.md, SECURITY.md read (VERIFIED)
- [x] Review current branch protection and rulesets. — `ZEAZDEV-PRODUCTION-GATE` id 26171864 active on `refs/heads/main`; required checks: CodeQL, dependency-review, repository-baseline; code-owner review NOT required; python/windows-python NOT required (GitHub API read-back, VERIFIED)
- [x] Identify all open PRs. — #3 (989af95, Draft), #5 (f19e339, Draft, dirty/mergeable=false), #6 (c356049, Draft, clean) (GitHub API, VERIFIED)
- [ ] Identify unresolved review comments. — PR #5 has CHANGES_REQUESTED on older head, not current SHA (UNVERIFIED for current SHA)
- [x] Establish release evidence directory or tracking system. — `docs/engineering/phase-0-repository-state-report.md` and `docs/engineering/phase-1-findings-register.md` created (VERIFIED)

**Acceptance Criteria:**
- [x] Repository state documented. — PHASE 0 report + PHASE 1 register (VERIFIED)
- [x] No user changes overwritten. — stash and worktrees preserved (VERIFIED)
- [x] No unexplained worktree or branch divergence. — PR #5 reconciled: base `feat/chatrdc-v1-foundation` (`989af95`) is now an ancestor of `staging/connectivity-first` (`407d134`); 0 commits behind, 10 ahead. Merge conflict resolved via normal non-force merge on 2026-11-04. (VERIFIED)
- [ ] All development work has traceable ownership. — commit f19e339 by cvsz on staging/connectivity-first (VERIFIED for this change)

### 0.2 Execution Status

| Status | Meaning |
|---|---|
| TODO | Not started |
| IN_PROGRESS | Implementation underway |
| BLOCKED | Waiting for dependency or authorization |
| IMPLEMENTED | Code completed |
| TESTED | Local tests passed |
| VERIFIED | Acceptance evidence confirmed |
| DEFERRED | Intentionally postponed |
| NOT_APPLICABLE | Not required, with documented reason |

---

# 1. REPOSITORY FOUNDATION

## 1.1 Source Code Quality

- [ ] Inspect complete source tree.
- [ ] Identify application entry points.
- [ ] Identify package boundaries.
- [ ] Identify duplicated logic.
- [ ] Identify circular dependencies.
- [ ] Identify dead code.
- [ ] Identify unsafe defaults.
- [ ] Identify incomplete implementations.
- [ ] Identify placeholder and TODO sections.
- [ ] Review exception handling.
- [ ] Review configuration management.
- [ ] Review dependency management.
- [ ] Review type annotations.
- [ ] Review coding standards.
- [ ] Establish maintainable module boundaries.

## 1.2 Development Environment

- [ ] Define supported Python versions.
- [ ] Verify Windows development environment.
- [ ] Verify Linux development environment.
- [ ] Verify WSL2 development environment.
- [ ] Verify dependency installation.
- [ ] Verify lockfile consistency.
- [ ] Verify reproducible builds.
- [ ] Verify development setup instructions.
- [ ] Verify test environment isolation.

## 1.3 Repository Quality Gates

- [x] Repository validator passes. — `python3 scripts/validate_repo.py` exit 0 ("Repository structure and local Markdown links are valid") with `.venv` present (VERIFIED; fix F3 applied)
- [x] Ruff passes. — `python -m ruff check agent mcp_server scripts/validate_repo.py tests/...` all checks passed (VERIFIED)
- [ ] Type checking passes, if configured. — no type checker configured in pyproject/Makefile/CI (NOT_APPLICABLE)
- [x] Unit tests pass. — `python -m pytest -q`: 41 passed, 3 subtests passed (VERIFIED; includes 4 new validator tests)
- [x] Package build succeeds. — `python -m build`: sdist + wheel `chatrdc-0.1.0` built (VERIFIED)
- [x] Dependency audit passes. — `python -m pip_audit`: no known vulnerabilities found; `pip check`: no broken requirements (VERIFIED via module; `pip-audit` console script shebang broken in relocated venv, F4)
- [ ] No accidental generated files. — untracked `package-lock.json` (empty npm lock in Python repo), `__pycache__`/`.venv`/`.ruff_cache` are gitignored (PARTIALLY VERIFIED; package-lock.json acknowledged, not committed)
- [x] No committed secrets. — CI secret-file-name check pattern targets `.env`/`id_rsa`/`*.pem`/`*.key`; only `.env.example` tracked; grep of tracked source found no hardcoded secrets (VERIFIED)
- [ ] No unexplained test exclusions. — no test exclusions found; all 41 tests run (VERIFIED)

**Acceptance Criteria:** Clean, reproducible, testable development baseline. — PARTIALLY VERIFIED (type checking N/A; package-lock.json acknowledged)

---

# 2. SYSTEM ARCHITECTURE

## 2.1 Architecture Definition

- [ ] Document current architecture.
- [ ] Document target architecture.
- [ ] Identify trust boundaries.
- [ ] Identify network boundaries.
- [ ] Identify component responsibilities.
- [ ] Define communication protocols.
- [ ] Define component lifecycle.
- [ ] Define failure handling.
- [ ] Define data flows.
- [ ] Define authentication flows.
- [ ] Define authorization flows.
- [ ] Define device identity lifecycle.
- [ ] Define upgrade compatibility.
- [ ] Define operational dependencies.

## 2.2 Component Architecture

- [ ] Local Agent architecture.
- [ ] MCP Server architecture.
- [ ] MCP Gateway architecture, if required.
- [ ] Desktop UI architecture.
- [ ] Device Registry architecture.
- [ ] Authentication architecture.
- [ ] Authorization architecture.
- [ ] Secure Connectivity architecture.
- [ ] Audit and Logging architecture.
- [ ] Monitoring architecture.
- [ ] Configuration architecture.
- [ ] Data Persistence architecture, if required.

## 2.3 Architecture Acceptance

- [ ] Architecture diagrams reflect actual implementation.
- [ ] API contracts are documented.
- [ ] Component boundaries are explicit.
- [ ] Security boundaries are documented.
- [ ] No undocumented public attack surface.
- [ ] Architecture decisions have recorded rationale.

---

# 3. LOCAL AGENT

## 3.1 Agent Core

- [ ] Agent startup.
- [ ] Agent shutdown.
- [ ] Graceful termination.
- [ ] Configuration loading.
- [ ] Configuration validation.
- [ ] Capability registry.
- [ ] Device identity.
- [ ] Local API.
- [ ] Health endpoint.
- [ ] Error handling.
- [ ] Structured logging.
- [ ] Resource limits.
- [ ] Process lifecycle monitoring.
- [ ] Crash recovery behavior.
- [ ] Signal handling.
- [ ] Version reporting.

## 3.2 Network Security

- [x] Bind to `127.0.0.1` by default. — `agent/__main__.py` uvicorn host="127.0.0.1" (VERIFIED)
- [x] Validate Host headers. — `agent/main.py` `_ALLOWED_HOSTS` loopback-only; `test_rejects_untrusted_host_header` (VERIFIED)
- [x] Validate Origin where relevant. — origin must match loopback host/port/scheme; `test_rejects_cross_origin_browser_request` etc. (VERIFIED)
- [x] Disable unsafe proxy-header trust. — `proxy_headers=False` in `__main__.py` and uvicorn.Config; MCP opener uses `ProxyHandler({})` (VERIFIED)
- [x] Protect against DNS rebinding. — `_is_loopback_peer` rejects non-loopback IPs; `test_rejects_non_loopback_peer`, forwarded-header override test (VERIFIED)
- [x] Protect against SSRF. — MCP connector loopback-only URL validation, `_NoRedirect` blocks off-loopback redirects, `_build_local_opener` ignores ambient proxies (VERIFIED)
- [x] Validate request sizes. — MCP `_get_json` bounds read to 256_000 bytes (VERIFIED)
- [x] Enforce request timeouts. — MCP connector `timeout=3.0` (VERIFIED)
- [ ] Enforce rate limits. — NOT implemented (P1 roadmap, deferred by SECURITY.md) (NOT_APPLICABLE to current scaffold)
- [x] Prevent unauthorized LAN exposure. — agent binds loopback only; middleware rejects non-loopback peers (VERIFIED)
- [x] Prevent unauthorized Internet exposure. — no public ingress; SECURITY.md documents agent must never be exposed directly (VERIFIED)
- [ ] Verify firewall behavior. — NOT tested (no Windows/Linux firewall environment available) (UNVERIFIED)

## 3.3 Agent Capabilities

- [x] System information. — `/api/v1/system` returns hostname, platform, release, python version, cpu_count, memory/disk (VERIFIED)
- [x] CPU and memory information. — cpu_count, memory_total_bytes, memory_available_bytes (VERIFIED)
- [x] Disk information. — disk_total_bytes, disk_free_bytes (VERIFIED)
- [ ] Network diagnostics. — NOT implemented (read-only scaffold) (NOT_APPLICABLE)
- [ ] Process inspection. — NOT implemented (read-only scaffold) (NOT_APPLICABLE)
- [ ] Service inspection. — NOT implemented (read-only scaffold) (NOT_APPLICABLE)
- [ ] Authorized service management. — NOT implemented; explicitly non-goal (NOT_APPLICABLE)
- [ ] Authorized process management. — NOT implemented; explicitly non-goal (NOT_APPLICABLE)
- [ ] Agent diagnostics. — health endpoint only (PARTIALLY VERIFIED)
- [ ] Capability permission enforcement. — NOT implemented (P1 roadmap) (NOT_APPLICABLE)

## 3.4 Agent Security

- [x] No arbitrary shell execution by default. — no shell/file-write/process-control tools exposed (VERIFIED)
- [x] No unrestricted filesystem access. — summary excludes home directory/env; no file access endpoints (VERIFIED)
- [x] No implicit privilege elevation. — agent runs as invoking user; no elevation (VERIFIED)
- [x] No hardcoded credentials. — no credentials in source (VERIFIED)
- [x] No sensitive information in logs. — access_log=False; no secrets logged (VERIFIED)
- [ ] Explicit permission for privileged operations. — NOT implemented (P1 roadmap) (NOT_APPLICABLE)
- [ ] Audit every sensitive operation. — NOT implemented (P1 roadmap) (NOT_APPLICABLE)
- [x] Verify unauthorized operations are denied. — non-loopback peers and untrusted Host/Origin rejected with 403 (VERIFIED)

**Acceptance Criteria:** Local Agent operates reliably with least privilege and a restricted capability model.

---

# 4. MCP SERVER AND CONNECTOR

## 4.1 MCP Protocol

- [x] Verify SDK and protocol versions. — `mcp>=2,<3` in pyproject; `mcp 2.3.0` installed (VERIFIED)
- [x] Initialization. — `MCPServer("Remote Desktop Commander")` (VERIFIED)
- [ ] Capability negotiation. — via MCP SDK; not separately tested (UNVERIFIED)
- [x] Tool registration. — `get_agent_health`, `get_system_summary` via `@mcp.tool()` (VERIFIED)
- [ ] Resource registration, if required. — not required, not implemented (NOT_APPLICABLE)
- [ ] Prompt registration, if required. — not required, not implemented (NOT_APPLICABLE)
- [ ] Input schemas. — tools take no parameters; trivial schema (PARTIALLY VERIFIED)
- [ ] Output schemas. — dict returns; not formally schema-constrained (PARTIALLY VERIFIED)
- [x] Error responses. — `RuntimeError("Local agent unavailable...")` on failure; no stack traces leaked (VERIFIED)
- [ ] Cancellation. — NOT implemented (NOT_APPLICABLE)
- [x] Timeouts. — `timeout=3.0` on agent HTTP request (VERIFIED)
- [ ] Session lifecycle. — stdio transport via SDK (PARTIALLY VERIFIED)
- [x] Connection cleanup. — connectivity test asserts agent thread shuts down cleanly (VERIFIED)
- [ ] Protocol compatibility tests. — not separately tested beyond direct tool calls (UNVERIFIED)

## 4.2 MCP Tool Security

- [x] Define tool purpose. — docstrings on both tools (VERIFIED)
- [x] Define strict input schema. — tools accept no parameters (VERIFIED)
- [x] Validate all parameters. — no parameters to validate (VERIFIED)
- [ ] Enforce capability permissions. — NOT implemented (P1 roadmap) (NOT_APPLICABLE)
- [ ] Enforce authorization. — NOT implemented (P1 roadmap) (NOT_APPLICABLE)
- [x] Bound execution time. — 3.0s agent request timeout (VERIFIED)
- [x] Bound resource consumption. — 256_000 byte response read bound (VERIFIED)
- [x] Document side effects. — read-only, no side effects (VERIFIED)
- [ ] Audit sensitive operations. — NOT implemented (P1 roadmap) (NOT_APPLICABLE)
- [ ] Test unauthorized calls. — NOT implemented (P1 roadmap) (NOT_APPLICABLE)
- [x] Test malformed requests. — `test_mcp_config` URL validation rejects non-loopback/ambiguous URLs (VERIFIED)
- [ ] Test oversized requests. — NOT implemented (NOT_APPLICABLE)

## 4.3 MCP Transport

- [x] Verify local stdio transport. — `mcp.run(transport="stdio")` in `__main__` (VERIFIED)
- [ ] Verify supported MCP host integration. — NOT done; no real MCP host connected (BLOCKED — P3 roadmap, requires end-to-end test)
- [ ] Define remote transport requirements. — NOT implemented (P1 roadmap) (NOT_APPLICABLE)
- [ ] Implement authenticated Streamable HTTP Gateway if required. — NOT implemented (P1 roadmap) (NOT_APPLICABLE)
- [ ] Configure TLS. — NOT implemented (P1 roadmap) (NOT_APPLICABLE)
- [ ] Implement session isolation. — NOT implemented (P1 roadmap) (NOT_APPLICABLE)
- [ ] Implement authentication. — NOT implemented (P1 roadmap) (NOT_APPLICABLE)
- [ ] Implement authorization. — NOT implemented (P1 roadmap) (NOT_APPLICABLE)
- [ ] Implement rate limiting. — NOT implemented (P1 roadmap) (NOT_APPLICABLE)
- [ ] Implement device routing. — NOT implemented (P1 roadmap) (NOT_APPLICABLE)
- [ ] Implement credential revocation. — NOT implemented (P1 roadmap) (NOT_APPLICABLE)
- [ ] Verify remote connection security. — NOT implemented (P1 roadmap) (NOT_APPLICABLE)

## 4.4 Integration Verification

- [ ] Test with a real MCP client. — NOT done; direct function calls only, not a real MCP host (UNVERIFIED)
- [ ] Test tool discovery. — NOT done (UNVERIFIED)
- [x] Test allowed read-only tool. — `test_connectivity.py` calls `get_agent_health`/`get_system_summary` against live agent (VERIFIED)
- [ ] Test denied unauthorized tool. — NOT implemented (P1 roadmap) (NOT_APPLICABLE)
- [x] Test disconnection. — `test_mcp_connector_reports_agent_disconnected` verifies RuntimeError (VERIFIED)
- [ ] Test reconnection. — NOT done (NOT_APPLICABLE)
- [ ] Test timeout. — timeout configured but timeout behavior not tested (UNVERIFIED)
- [ ] Test error propagation. — disconnected-agent path tested (VERIFIED for that path)
- [x] Record exact integration environment and version. — Python 3.14.4, mcp 2.3.0, Linux (VERIFIED)

**Acceptance Criteria:** Real MCP integration works and enforces the documented security model.

---

# 5. DEVICE IDENTITY AND ENROLLMENT

## 5.1 Device Registry

- [ ] Unique device identifier.
- [ ] Device metadata.
- [ ] Device operating system.
- [ ] Agent version.
- [ ] Device status.
- [ ] Last-seen timestamp.
- [ ] Connection status.
- [ ] Device ownership.
- [ ] Device groups, if required.
- [ ] Device search.
- [ ] Device filtering.

## 5.2 Enrollment

- [ ] Enrollment workflow.
- [ ] Short-lived enrollment token.
- [ ] Single-use token where appropriate.
- [ ] Cryptographic device identity.
- [ ] Secure credential issuance.
- [ ] Device ownership validation.
- [ ] Enrollment audit event.
- [ ] Enrollment failure handling.
- [ ] Duplicate enrollment handling.
- [ ] Re-enrollment workflow.

## 5.3 Revocation

- [ ] Device revocation.
- [ ] Credential invalidation.
- [ ] Session termination.
- [ ] Revocation audit event.
- [ ] Revoked device denied access.
- [ ] Re-enrollment after revocation.
- [ ] Credential rotation.

**Acceptance Criteria:** Devices cannot access the platform without valid, authorized identity and enrollment.

---

# 6. AUTHENTICATION AND AUTHORIZATION

## 6.1 Authentication

- [ ] Administrator authentication.
- [ ] User authentication.
- [ ] Device authentication.
- [ ] Session management.
- [ ] Session expiration.
- [ ] Credential rotation.
- [ ] Credential revocation.
- [ ] Brute-force protection.
- [ ] Rate limiting.
- [ ] Secure credential storage.
- [ ] Secure logout.
- [ ] Authentication audit events.

## 6.2 RBAC

- [ ] Define Administrator role.
- [ ] Define Organization Administrator role, if multi-tenant.
- [ ] Define Device Administrator role.
- [ ] Define Operator role.
- [ ] Define Auditor role.
- [ ] Define Read-Only role.
- [ ] Implement role permissions.
- [ ] Implement resource-level permissions.
- [ ] Implement action-level permissions.
- [ ] Enforce authorization server-side.
- [ ] Test privilege escalation.
- [ ] Test unauthorized device access.

## 6.3 Tenant Isolation

- [ ] Define tenant identity, if multi-tenant.
- [ ] Enforce tenant-scoped queries.
- [ ] Enforce tenant-scoped device access.
- [ ] Isolate credentials.
- [ ] Isolate audit records.
- [ ] Test cross-tenant access.
- [ ] Test tenant ID spoofing.
- [ ] Test tenant-level administrator boundaries.

**Acceptance Criteria:** Every protected operation requires an authorized identity and explicit permission.

---

# 7. DESKTOP MANAGEMENT UI

## 7.1 Core UI

- [ ] Application startup.
- [ ] Application shutdown.
- [ ] Dashboard.
- [ ] Device list.
- [ ] Device details.
- [ ] Device status.
- [ ] Agent status.
- [ ] Connection status.
- [ ] Capability list.
- [ ] Permission visibility.
- [ ] Operation history.
- [ ] Audit history.
- [ ] Configuration management.
- [ ] Error notifications.
- [ ] Loading states.
- [ ] Empty states.

## 7.2 UX and Reliability

- [ ] Responsive UI.
- [ ] No blocking network calls on UI thread.
- [ ] Correct async execution.
- [ ] Safe background task lifecycle.
- [ ] Connection state synchronization.
- [ ] Operation progress.
- [ ] Operation cancellation.
- [ ] Explicit confirmation for sensitive actions.
- [ ] Clear permission-denied messages.
- [ ] Accessibility review.
- [ ] Keyboard navigation.
- [ ] UI state recovery after reconnect.

## 7.3 UI Security

- [ ] Do not trust UI-only authorization.
- [ ] Do not expose secrets.
- [ ] Do not store credentials insecurely.
- [ ] Do not display sensitive data unnecessarily.
- [ ] Confirm privileged operations.
- [ ] Reflect actual server/agent results.
- [ ] Prevent duplicate sensitive submissions.

**Acceptance Criteria:** UI accurately reflects runtime state and cannot bypass backend security controls.

---

# 8. REMOTE DESKTOP AND ADVANCED OPERATIONS

## 8.1 Capability Definition

- [ ] Device discovery.
- [ ] Device status.
- [ ] System diagnostics.
- [ ] Process inspection.
- [ ] Service inspection.
- [ ] Authorized service management.
- [ ] Authorized file operations.
- [ ] Remote terminal design review.
- [ ] Desktop viewing design review.
- [ ] Desktop control design review.
- [ ] Remote assistance design review.

## 8.2 High-Risk Operations

- [ ] Explicit authorization model.
- [ ] Session-level permissions.
- [ ] User confirmation.
- [ ] Encrypted transport.
- [ ] Session isolation.
- [ ] Operation audit.
- [ ] Timeout enforcement.
- [ ] Resource limits.
- [ ] Emergency termination.
- [ ] Device revocation handling.
- [ ] Session revocation handling.
- [ ] Platform-specific security review.

**Acceptance Criteria:** No high-risk operation is enabled without its own security design and verified tests.

---

# 9. DATABASE AND DATA GOVERNANCE

## 9.1 Persistence

- [ ] Determine actual persistence requirements.
- [ ] Select database architecture.
- [ ] Define data models.
- [ ] Define schema migrations.
- [ ] Define transaction boundaries.
- [ ] Define connection lifecycle.
- [ ] Define concurrency behavior.
- [ ] Define retention.
- [ ] Define deletion.
- [ ] Define backup strategy.
- [ ] Define restore strategy.

## 9.2 Data Protection

- [ ] Classify sensitive data.
- [ ] Inventory PII.
- [ ] Minimize collected data.
- [ ] Secure credentials.
- [ ] Protect audit data.
- [ ] Protect backups.
- [ ] Define retention periods.
- [ ] Define deletion procedures.
- [ ] Prevent secrets in logs.
- [ ] Test backup integrity.
- [ ] Test restore procedure.

**Acceptance Criteria:** Persistent data is protected, recoverable, and governed by documented policies.

---

# 10. SECURE CONNECTIVITY

## 10.1 Connectivity Layer

- [ ] Define LAN connection behavior.
- [ ] Define private-network behavior.
- [ ] Define remote gateway behavior.
- [ ] Define connection authentication.
- [ ] Define connection authorization.
- [ ] Define TLS configuration.
- [ ] Define device routing.
- [ ] Define session isolation.
- [ ] Define reconnect behavior.
- [ ] Define disconnect cleanup.
- [ ] Define timeout handling.
- [ ] Define network-change behavior.

## 10.2 Network Security

- [ ] No direct public exposure of local Agent.
- [ ] No unauthenticated remote endpoint.
- [ ] No trust in client-supplied device identity.
- [ ] Validate certificates.
- [ ] Prevent unauthorized gateway access.
- [ ] Apply rate limits.
- [ ] Apply request size limits.
- [ ] Apply session limits.
- [ ] Audit remote access.
- [ ] Test revoked credentials.
- [ ] Test interrupted connections.

**Acceptance Criteria:** Remote access is mediated by authenticated, authorized, encrypted infrastructure.

---

# 11. WINDOWS / LINUX / WSL2

## 11.1 Windows

- [ ] Windows installation.
- [ ] Windows startup.
- [ ] Windows shutdown.
- [ ] Windows process permissions.
- [ ] Windows Firewall behavior.
- [ ] UAC behavior.
- [ ] Windows credential storage.
- [ ] Windows logging.
- [ ] Windows upgrade.
- [ ] Windows uninstall.
- [ ] Windows recovery.
- [ ] Installer signature verification, if distributed.

## 11.2 Linux

- [ ] Linux installation.
- [ ] Linux startup.
- [ ] systemd integration, if applicable.
- [ ] Dedicated service account.
- [ ] File permissions.
- [ ] Network restrictions.
- [ ] Linux logging.
- [ ] Linux upgrade.
- [ ] Linux uninstall.
- [ ] Linux recovery.

## 11.3 WSL2

- [ ] WSL2 installation.
- [ ] WSL2 networking.
- [ ] Windows-to-WSL connectivity.
- [ ] WSL-to-Windows connectivity.
- [ ] Localhost forwarding behavior.
- [ ] Firewall behavior.
- [ ] Filesystem boundaries.
- [ ] Process lifecycle.
- [ ] WSL restart behavior.
- [ ] WSL shutdown behavior.
- [ ] Recovery after network changes.

**Acceptance Criteria:** Each supported platform has actual test evidence and documented limitations.

---

# 12. SECURITY TESTING

## 12.1 Application Security

- [ ] Injection testing.
- [ ] Command injection testing.
- [ ] Path traversal testing.
- [ ] SSRF testing.
- [ ] DNS rebinding testing.
- [ ] Host header testing.
- [ ] Origin validation testing.
- [ ] Proxy-header spoofing testing.
- [ ] Unsafe deserialization testing.
- [ ] Authentication bypass testing.
- [ ] Authorization bypass testing.
- [ ] Privilege escalation testing.
- [ ] Session security testing.
- [ ] Resource exhaustion testing.
- [ ] Race condition testing.

## 12.2 Secret and Supply Chain Security

- [ ] Secret scanning.
- [ ] Dependency vulnerability scanning.
- [ ] License scanning.
- [ ] SBOM generation.
- [ ] Lockfile validation.
- [ ] CodeQL.
- [ ] Dependency Review.
- [ ] Container scanning, if applicable.
- [ ] Artifact integrity verification.
- [ ] Build provenance, where supported.

## 12.3 Threat Model

- [ ] STRIDE or equivalent threat model.
- [ ] Asset inventory.
- [ ] Trust boundary inventory.
- [ ] Attack surface inventory.
- [ ] Threat scenarios.
- [ ] Risk assessment.
- [ ] Mitigation mapping.
- [ ] Residual risk documentation.
- [ ] Security exception process.

**Acceptance Criteria:** No unresolved critical vulnerability or unapproved high-risk security finding.

---

# 13. TEST AUTOMATION AND QUALITY ASSURANCE

## 13.1 Unit Tests

- [ ] Agent tests.
- [ ] Configuration tests.
- [ ] Capability tests.
- [ ] MCP tests.
- [ ] Authentication tests.
- [ ] Authorization tests.
- [ ] Device identity tests.
- [ ] Policy tests.
- [ ] Error handling tests.
- [ ] UI logic tests.

## 13.2 Integration Tests

- [ ] Agent-to-MCP tests.
- [ ] Agent lifecycle tests.
- [ ] Device enrollment tests.
- [ ] Device revocation tests.
- [ ] Authentication integration.
- [ ] Authorization integration.
- [ ] Database integration, if applicable.
- [ ] Gateway integration, if applicable.
- [ ] Session lifecycle tests.
- [ ] Recovery tests.

## 13.3 E2E Tests

- [ ] Install agent.
- [ ] Start agent.
- [ ] Verify health.
- [ ] Enroll device.
- [ ] Authenticate.
- [ ] Discover device.
- [ ] Discover capabilities.
- [ ] Execute authorized read-only operation.
- [ ] Verify audit record.
- [ ] Disconnect.
- [ ] Reconnect.
- [ ] Revoke device.
- [ ] Verify access denial.

## 13.4 Performance Tests

- [ ] Agent startup latency.
- [ ] MCP request latency.
- [ ] Connection establishment latency.
- [ ] Concurrent session behavior.
- [ ] Memory consumption.
- [ ] CPU consumption.
- [ ] Long-running stability.
- [ ] Resource exhaustion behavior.
- [ ] Recovery under load.

## 13.5 Test Quality

- [ ] No unexplained skipped tests.
- [ ] No hidden test exclusions.
- [ ] No fabricated mocks for real integration claims.
- [ ] Test isolation verified.
- [ ] Flaky tests identified.
- [ ] Failure diagnostics available.
- [ ] Coverage measured.
- [ ] Critical paths covered.

**Acceptance Criteria:** All required automated tests pass on the exact candidate SHA.

---

# 14. OBSERVABILITY AND SRE

## 14.1 Logging

- [ ] Structured logging.
- [ ] Correlation IDs.
- [ ] Request IDs.
- [ ] Device identifiers where safe.
- [ ] Operation result.
- [ ] Duration.
- [ ] Error classification.
- [ ] Secret redaction.
- [ ] PII minimization.
- [ ] Log retention policy.

## 14.2 Metrics

- [ ] Agent uptime.
- [ ] Connection success rate.
- [ ] Connection latency.
- [ ] MCP request latency.
- [ ] Authentication failures.
- [ ] Authorization denials.
- [ ] Active sessions.
- [ ] Operation failures.
- [ ] Resource consumption.
- [ ] Error rate.

## 14.3 Reliability

- [ ] Timeout policy.
- [ ] Retry policy.
- [ ] Exponential backoff.
- [ ] Jitter.
- [ ] Idempotent operations.
- [ ] Graceful shutdown.
- [ ] Circuit breaker, where justified.
- [ ] Backpressure.
- [ ] Recovery after restart.
- [ ] Dependency failure handling.

## 14.4 Disaster Recovery

- [ ] Backup strategy.
- [ ] Restore procedure.
- [ ] Backup integrity verification.
- [ ] RTO definition.
- [ ] RPO definition.
- [ ] Recovery exercise.
- [ ] Incident response procedure.
- [ ] Credential compromise procedure.
- [ ] Device compromise procedure.

**Acceptance Criteria:** System health and failures are observable, and recovery is tested.

---

# 15. CI/CD AND GITHUB GOVERNANCE

## 15.1 CI Pipeline

- [ ] Repository validation.
- [ ] Formatting.
- [ ] Linting.
- [ ] Type checking.
- [ ] Unit tests.
- [ ] Integration tests.
- [ ] Security tests.
- [ ] Package build.
- [ ] Dependency audit.
- [ ] CodeQL.
- [ ] Dependency Review.
- [ ] Secret scanning.
- [ ] SBOM generation.
- [ ] Artifact verification.

## 15.2 Cross-Platform CI

- [ ] Linux CI.
- [ ] Windows CI.
- [ ] Supported Python versions.
- [ ] WSL2 verification plan.
- [ ] Platform-specific tests.
- [ ] Build artifact verification.

## 15.3 PR Governance

- [ ] PR objective documented.
- [ ] Exact head SHA recorded.
- [ ] Full diff inspected.
- [ ] Tests linked to exact SHA.
- [ ] Security impact documented.
- [ ] Review comments resolved.
- [ ] `policedbc` independent review.
- [ ] Required approval verified.
- [ ] Last-push approval requirement satisfied.
- [ ] Required checks passed.
- [ ] `cvsz` authorized merge only after gates pass.

## 15.4 Branch Protection

- [ ] Inspect effective ruleset.
- [ ] Require applicable CI checks.
- [ ] Require security checks.
- [ ] Require independent approval.
- [ ] Require resolved review threads.
- [ ] Dismiss stale reviews.
- [ ] Protect against unauthorized force-push.
- [ ] Protect against branch deletion.
- [ ] Verify bypass actors.
- [ ] Verify release branch protection.

**Acceptance Criteria:** No merge occurs without exact-SHA verification and independent governance approval.

---

# 16. DOCUMENTATION

- [ ] README.md.
- [ ] Architecture documentation.
- [ ] Installation guide.
- [ ] Configuration guide.
- [ ] Security model.
- [ ] Threat model.
- [ ] MCP integration guide.
- [ ] Device enrollment guide.
- [ ] Authentication guide.
- [ ] Authorization guide.
- [ ] API and protocol documentation.
- [ ] Windows deployment guide.
- [ ] Linux deployment guide.
- [ ] WSL2 guide.
- [ ] Troubleshooting.
- [ ] Operations guide.
- [ ] Backup and restore.
- [ ] Upgrade guide.
- [ ] Rollback guide.
- [ ] Security incident response.
- [ ] Release notes.
- [ ] Known limitations.
- [ ] Thai documentation where required.

**Acceptance Criteria:** Documentation accurately represents tested functionality.

---

# 17. RELEASE ENGINEERING

## 17.1 Version and Build

- [ ] Confirm versioning strategy.
- [ ] Confirm package version.
- [ ] Confirm application version.
- [ ] Confirm MCP version compatibility.
- [ ] Build source distribution.
- [ ] Build wheel.
- [ ] Build Windows installer, if supported.
- [ ] Build Linux package, if supported.
- [ ] Verify artifacts.
- [ ] Generate SHA256 checksums.
- [ ] Generate SBOM.
- [ ] Verify signing, if supported.
- [ ] Verify release metadata.

## 17.2 Release Documentation

- [ ] Changelog.
- [ ] Release notes.
- [ ] Breaking changes.
- [ ] Migration steps.
- [ ] Supported platforms.
- [ ] Security changes.
- [ ] Known limitations.
- [ ] Installation instructions.
- [ ] Rollback instructions.

## 17.3 Release Governance

- [ ] Final exact SHA recorded.
- [ ] All required tests passed.
- [ ] All required CI passed.
- [ ] Security checks passed.
- [ ] Independent review approved.
- [ ] All threads resolved.
- [ ] Ruleset satisfied.
- [ ] Release artifacts verified.
- [ ] Rollback plan approved.
- [ ] Release publication authorized.

**Acceptance Criteria:** A reproducible, independently reviewed release candidate exists with verified artifacts.

---

# 18. PRODUCTION DEPLOYMENT

## 18.1 Pre-Deployment

- [ ] Target environment identified.
- [ ] Deployment SHA identified.
- [ ] Configuration reviewed.
- [ ] Secrets verified.
- [ ] TLS verified.
- [ ] Firewall verified.
- [ ] Authentication verified.
- [ ] Authorization verified.
- [ ] Network exposure reviewed.
- [ ] Backup verified.
- [ ] Rollback tested.
- [ ] Monitoring available.
- [ ] Deployment authorization obtained.

## 18.2 Deployment

- [ ] Deploy approved artifact.
- [ ] Verify artifact checksum.
- [ ] Verify runtime version.
- [ ] Verify service startup.
- [ ] Verify readiness.
- [ ] Verify liveness.
- [ ] Verify agent connectivity.
- [ ] Verify MCP connectivity.
- [ ] Verify authentication.
- [ ] Verify authorization.
- [ ] Verify audit logging.

## 18.3 Post-Deployment

- [ ] Verify actual deployment SHA.
- [ ] Verify actual artifact SHA256.
- [ ] Verify application health.
- [ ] Verify operational metrics.
- [ ] Verify error rates.
- [ ] Verify network restrictions.
- [ ] Verify access revocation.
- [ ] Verify recovery behavior.
- [ ] Verify rollback readiness.
- [ ] Record production evidence.

**Acceptance Criteria:** Actual production deployment is independently verifiable and operationally stable.

---

# 19. FINAL RELEASE GATES

| Gate | Acceptance Criteria | Status |
|---|---|---|
| G0 | Repository integrity verified | VERIFIED — PHASE 0 report; git + GitHub API inspection; worktrees/stash preserved |
| G1 | Architecture and threat model reviewed | PARTIALLY VERIFIED — architecture docs reviewed; threat model NOT authored (deferred P1) |
| G2 | Core functionality complete | VERIFIED — read-only agent + MCP + dashboard + live connectivity tests pass |
| G3 | Authentication and authorization verified | BLOCKED — NOT implemented by design; P1 roadmap, deferred by SECURITY.md |
| G4 | Agent and MCP integration verified | VERIFIED — live loopback TCP tests: dashboard, /health, /api/v1/system, MCP health/system, disconnected-agent path |
| G5 | Windows/Linux/WSL2 verified | UNVERIFIED — only Linux (this env) tested; Windows/WSL2 not performed |
| G6 | Required tests passed | VERIFIED — 41 passed + 3 subtests; ruff; build; pip-audit; validator; bootstrap |
| G7 | CI/CD and supply chain passed | PARTIALLY VERIFIED — local checks pass; GitHub Actions status pending/0 on f19e339 (Actions not yet run on exact head) |
| G8 | Independent review and governance passed | BLOCKED — PR #5 dirty/mergeable=false (42 behind base); no policedbc approval on f19e339 |
| G9 | Release artifacts and rollback verified | NOT_APPLICABLE — only local sdist/wheel built; no release authorized |
| G10 | Authorized production deployment verified | NOT_APPLICABLE — no deployment authorization; not production-ready |

No gate may be marked VERIFIED without evidence.

---

# 20. RELEASE ACCEPTANCE MATRIX

| Category | Required Result |
|---|---|
| Repository | Clean and traceable |
| Architecture | Documented and implemented |
| Local Agent | Secure and reliable |
| MCP | Real integration verified |
| Device Identity | Enrollment and revocation verified |
| Authentication | Verified |
| Authorization | Verified |
| UI | Functional and secure |
| Connectivity | Authenticated and encrypted |
| Windows | Verified on supported versions |
| Linux | Verified on supported versions |
| WSL2 | Verified with documented limitations |
| Security | No unresolved critical findings |
| Tests | All required tests passed |
| CI | All required checks passed |
| Governance | Independent approval verified |
| Artifacts | Reproducible and integrity-checked |
| Documentation | Complete and accurate |
| Rollback | Tested |
| Deployment | Explicitly authorized |
| Production | Runtime evidence verified |

---

# 21. FINAL STATUS CLASSIFICATION

Select only the highest state supported by evidence.

- [ ] BLOCKED
- [x] IN PROGRESS — overall effort ongoing (P1 security gates, PR reconciliation, cross-platform)
- [x] CODE COMPLETE — read-only scaffold implementation scope complete
- [x] TEST VERIFIED — required local tests passed: 41 passed + 3 subtests
- [ ] CI VERIFIED — GitHub Actions status pending/0 on f19e339; required checks (CodeQL, dependency-review, repository-baseline) not yet run on exact head
- [ ] RELEASE CANDIDATE — G7/G8 blocked
- [ ] RELEASE READY — G3/G8 blocked
- [ ] DEPLOYED — no deployment authorization
- [ ] PRODUCTION VERIFIED — no deployment authorization

Definitions:

**CODE COMPLETE:** Implementation scope completed, but tests may remain.

**TEST VERIFIED:** Required local and integration tests passed.

**CI VERIFIED:** Required CI checks passed on the exact SHA.

**RELEASE CANDIDATE:** Release artifacts built and release gates are being finalized.

**RELEASE READY:** Required release gates and independent governance approval passed.

**DEPLOYED:** Authorized deployment completed.

**PRODUCTION VERIFIED:** Actual deployed runtime, security controls, integration, health, and operational acceptance verified.

---

# 22. FINAL EXECUTION RULES

1. Execute checklist items in dependency order.
2. Inspect before modifying.
3. Preserve all existing user work.
4. Fix root causes.
5. Prefer the smallest safe implementation.
6. Add tests for every meaningful fix.
7. Run verification after every relevant change.
8. Record exact commit SHAs.
9. Require independent review.
10. Never self-approve.
11. Never bypass branch protection.
12. Never force-push.
13. Never delete unmerged work.
14. Never claim unsupported functionality.
15. Never expose the Local Agent directly to the Internet.
16. Never enable unrestricted remote shell execution.
17. Never deploy without explicit authorization.
18. Never publish an unverified release.
19. Document residual risks.
20. Report actual evidence, not assumptions.

**FINAL OBJECTIVE**

Deliver ChatRDC as a genuinely secure, reliable, maintainable, observable, cross-platform Enterprise Remote Desktop Management Platform.

**Engineering Principle:**

Evidence over claims.  
Security over convenience.  
Reliability over shortcuts.  
Governance over speed.  
Production verification over marketing claims.