# PHASE 1 — Prioritized Findings Register

**chatrdc — Remote Desktop Commander**  
Basis: PHASE 0 repository inspection + local verification (Python 3.14.4)  
Severity scale: P0 critical security/data-loss · P1 major functional/reliability · P2 reliability/maintainability · P3 quality · P4 optional

---

## Findings

### F1 — Branch divergence blocks PR #5 merge (P1)
**Affected:** `staging/connectivity-first` (current HEAD `0183e70`, open PR #5)  
**Evidence:** GitHub API: PR #5 head `0183e70`, base `feat/chatrdc-v1-foundation` `8773305`, 7 commits ahead / 42 behind, `mergeable=false`, `mergeable_state=dirty`, `rebaseable=false`. Also local `main` (`a4f20c6`) is 1 commit behind `origin/main` (`52fbad7`).  
**Impact:** PR #5 cannot be merged until reconciled with its base without force-push. Current checkout cannot be cleanly merged to main either.  
**Remediation:** Reconcile `staging/connectivity-first` onto its current base via a normal (non-force) update, inspect the full resulting diff, re-run all checks on the exact final head, then obtain fresh independent review. Do not rebase/force-push shared branches.  
**Status:** UNVERIFIED (no reconciliation attempted; blocked on careful branch archaeology)

### F2 — Orphaned/broken worktree (P2)
**Affected:** `/home/cvsz/chatrdc-connectivity-signed` (`feat/connectivity-first-signed`)  
**Evidence:** `.git` gitdir references `/home/cvsz/chatrdc-upstream/.git/worktrees/chatrdc-connectivity-signed`, which does not exist; `git` commands in that directory fail with "not a git repository".  
**Impact:** That worktree's state cannot be inspected or used via git until its gitdir is restored or the worktree is removed.  
**Remediation:** Do NOT delete or reset (instruction: no destructive worktree ops without authorization). Document as blocked; resolve only with explicit authorization.  
**Status:** BLOCKED (requires authorization to repair/remove)

### F3 — Repository validator walks `.venv` and other generated dirs, causing local false positives (P2)
**Affected:** `scripts/validate_repo.py`  
**Evidence:** Local run of `python3 scripts/validate_repo.py` returned exit 1 with broken-link errors exclusively under `.venv/lib/python3.14/site-packages/**/README.md` (dependency files). CI runs `validate_repo.py` on a fresh checkout before dependency installation, so CI is unaffected; local `make validate-template` fails when a venv is present.  
**Impact:** False-positive validation failures in local development; masks real broken links among repo-owned Markdown.  
**Remediation:** Skip generated/dependency/cache directories (`.venv`, `build`, `dist`, `__pycache__`, `.pytest_cache`, `.ruff_cache`, `.mypy_cache`, `.cache`, `coverage`, `node_modules`, `.next`, `.nuxt`, `.out`, `tmp`, `.tmp`) in the Markdown link scan; add a unit test confirming a repo-owned Markdown broken link is still caught while a `.venv` broken link is skipped.  
**Status:** IN PROGRESS (fix + test planned below)

### F4 — `pip-audit` console script shebang broken in local venv (P2, environment)
**Affected:** `.venv/bin/pip-audit`  
**Evidence:** Shebang `#!/home/cvsz/chatrdc-upstream/.venv/bin/python` (nonexistent path). `python -m pip_audit` works: "No known vulnerabilities found".  
**Impact:** `make security` (`pip-audit`) fails locally in this relocated venv. Fresh CI venv would not have this problem. Not a repository code defect.  
**Remediation:** Document; recreate venv or reinstall pip-audit locally if needed. No repo change required.  
**Status:** UNVERIFIED for repo CI (environment-only)

### F5 — Untracked stray `package-lock.json` (P3)
**Affected:** Repository root  
**Evidence:** Untracked `package-lock.json` (108 bytes, `{"name":"chatrdc","lockfileVersion":3,"requires":true,"packages":{}}`) in a Python-only project.  
**Impact:** Harmless but confusing; not part of the Python supply chain.  
**Remediation:** Acknowledge; remove if confirmed accidental (not a tracked file; deletion is low-risk but should be deliberate).  
**Status:** UNVERIFIED (not yet decided)

### F6 — P1 security/product scope gaps (correctly deferred, not defects) (P1 scope)
**Affected:** Product scope  
**Evidence:** README/SECURITY.md/architecture/docs/roadmap: no authentication, device enrollment, RBAC/deny-by-default, TLS gateway, audit logging, rate limiting, remote desktop transport/view/control, signed installers, SBOM, or ChatGPT integration. These are P1 roadmap items.  
**Impact:** Product is not production-ready and not remotely accessible by design.  
**Remediation:** Implement only after threat model, authentication/authorization design, gateway/TLS design, and independent security review. Do NOT implement ad hoc.  
**Status:** NOT APPLICABLE to current release (deferred by design)

---

## Security scan results

- `pip-audit` (via `python -m pip_audit`): No known vulnerabilities in resolved third-party dependencies. Local `chatrdc` package not on PyPI, not audited as registry package.
- Ruff lint + format: clean.
- No hardcoded secrets or credentials found in tracked source (secret-file-name CI check pattern targets `.env`, `id_rsa`, `*.pem`, `*.key`; only `.env.example` is tracked, which is allowed).
- CodeQL/Dependency Review/repository-baseline: required by ruleset on `main`; live CI run IDs not currently obtainable via read-only API (commit status endpoint returns pending/0 for inspected SHAs).

---

## Recommended immediate action

Address **F3** (validate_repo.py directory exclusion) as the smallest safe, reviewable change with test coverage, then re-run `make ci`-equivalent checks and record evidence. Defer F1/F2 pending careful branch reconciliation and authorization. Defer F6 (P1 security scope) pending reviewed design.
