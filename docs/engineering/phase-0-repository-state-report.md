# PHASE 0 — Repository State Report

**chatrdc — Remote Desktop Commander**  
Repository: https://github.com/cvsz/chatrdc (git@github.com:cvsz/chatrdc.git)  
Classification: Evidence-based, non-production scaffold  
Executed: 2026-11-04 (local environment, Linux, Python 3.14.4)

---

## A. Git and worktree state

| Item | Value |
|---|---|
| Working directory | /home/cvsz/chatrdc |
| Active branch | `staging/connectivity-first` |
| HEAD SHA | `0183e70235802e7a43271bd6295e14a6fecbc921` |
| HEAD subject | docs: add English repository engineering governance guide |
| Remote tracking | `origin/staging/connectivity-first` == HEAD (in sync) |
| Working tree | Clean except untracked `package-lock.json` |
| Untracked files | `package-lock.json` (108 bytes, empty npm lockfile; Python-only repo) |
| Stash | `stash@{0}`: "WIP: preserve local MCP config test changes before upstream sync" (modifies `tests/test_mcp_config.py`). Preserved, not applied. |
| Git user | cvsz / seaza@msn.com |

## B. Branches (local vs origin)

| Branch | Local SHA | Origin SHA | Relation to origin |
|---|---|---|---|
| `main` | `a4f20c6` (Initial commit) | `52fbad7` (fix(ci): align CodeQL action versions (#4)) | **Local 1 commit behind origin** (fast-forwardable; not synced, documented) |
| `feat/chatrdc-v1-foundation` | `0eaafea` | `989af95` | Local ahead 1 / behind 42 |
| `staging/connectivity-first` | `0183e70` | `0183e70` | In sync (current checkout) |
| `feat/connectivity-first-signed` | `0eaafea` | — | Tied to broken worktree (see worktrees) |

## C. Worktrees

| Worktree | State | Notes |
|---|---|---|
| /home/cvsz/chatrdc | `0183e70` [staging/connectivity-first] | Primary checkout. Healthy. |
| /home/cvsz/chatrdc-connectivity-signed | `0eaafea` [feat/connectivity-first-signed] | **BROKEN**: `.git` gitdir references `/home/cvsz/chatrdc-upstream/.git/worktrees/chatrdc-connectivity-signed`, which does not exist. Orphaned worktree. Not touched (no destructive ops without authorization). |
| /home/cvsz/chatrdc-validator | `c356049` (detached HEAD) | PR #6 head (`fix: exclude generated directories from markdown validation`). Healthy. |

## D. Open pull requests (via GitHub API, read-only)

| PR | Branch | Head SHA | Base | State | Mergeable | Notes |
|---|---|---|---|---|---|---|
| #3 | feat/chatrdc-v1-foundation | `989af95` | main `a4f20c6` | Draft | true / clean | 93 commits ahead / 1 behind main. Historical CI/CodeQL/Dependency-Review runs claimed (59/55/54); live commit-status API returns `pending` / 0 statuses for `989af95`. policedbc APPROVED 2026-10-30, then CHANGES_REQUESTED 2026-11-01 (base-branch drift). Keep Draft; do not merge. |
| #5 | staging/connectivity-first | `0183e70` (current HEAD) | feat/chattd-v1-foundation `8773305` | Draft | **false / dirty / not rebaseable** | 7 commits ahead / 42 behind base. Latest review CHANGES_REQUESTED on an older head. Cannot merge until reconciled with base. |
| #6 | fix/validator-skip-generated-dirs | `c356049` | staging/connectivity-first `0183e70` | Draft | true / clean | 1 commit. Requested reviewer: policedbc. Claims CI run #61 passed, local `make ci` passed, pytest 37 passed, pip-audit clean, build passed. Live status `pending` / 0. |

## E. Ruleset (effective, provider read-back)

Ruleset `ZEAZDEV-PRODUCTION-GATE` (id `26171864`), enforcement **active**, applies to `refs/heads/main`:

- Pull request: 1 approving review; dismiss stale reviews on push; require last-push approval; require review thread resolution; require extra approval for unattributed changes; **code-owner review NOT required**.
- Required status checks (strict): `CodeQL`, `dependency-review`, `repository-baseline`.
- Does **NOT** require `python` or `windows-python` CI checks (gap noted in historical observation; not corrected in current ruleset).
- Deletion and non-fast-forward rules enabled.

## F. Local verification evidence (Python 3.14.4, `.venv`)

| Command | Exit code | Result |
|---|---|---|
| `python -m pip check` | 0 | No broken requirements found |
| `python -m ruff check agent mcp_server tests/...` | 0 | All checks passed |
| `python -m ruff format --check agent mcp_server tests/...` | 0 | 7 files already formatted |
| `python -m pytest -q` | 0 | 37 passed, 3 subtests passed |
| `python -m build` | 0 | sdist + wheel built (`chatrdc-0.1.0`) |
| `python -m pip_audit` | 0 | No known vulnerabilities found (`pip-audit` console script has a broken shebang pointing to relocated venv; works via module) |
| `python3 scripts/validate_repo.py` | 1 (locally) | Reports broken links **only inside `.venv`** (dependency READMEs) — false positive from local venv; CI runs this pre-install on a fresh checkout, so CI is unaffected. Validator does not exclude `.venv`/build/dist/cache dirs. |
| `python -m unittest discover -s tests -p 'test_bootstrap.py' -v` | 0 | 5 tests OK |

## G. Product scope (implemented vs target)

Implemented (verified): loopback-only FastAPI agent (`127.0.0.1:8765`, `proxy_headers=False`), read-only `/health` and `/api/v1/system`, local dashboard, Host/Origin validation, stdio MCP connector with 2 read-only tools (`get_agent_health`, `get_system_summary`), loopback-only MCP agent URL validation, redirect blocking, ambient proxy disabled, bounded reads, 3s timeout, unit + live connectivity tests.

Not implemented (correctly deferred per SECURITY.md/roadmap): authentication, device enrollment, RBAC/deny-by-default, TLS gateway, audit logging, rate limiting, remote desktop transport/view/control, signed installers, SBOM, ChatGPT integration, production deployment.

Version: `0.1.0` (pyproject.toml).

**Release readiness:** Not production-ready. This is a read-only local scaffold. P1 identity/remote-access gates are unimplemented and correctly gated.

## H. Branch protection note

Local `main` is one commit behind `origin/main`. No force-push, reset, or destructive Git operation was performed. All worktrees and the stash are preserved.

---

## I. Evidence-state classification (ZEAZ)

- Repository/Git state: VERIFIED (direct git + GitHub API inspection)
- Local checks (lint/format/test/build/audit/bootstrap): VERIFIED (commands run locally, exit code 0)
- CI check claims on PR heads: UNVERIFIED (live commit-status API returns pending/0; historical run numbers are claims, not current evidence)
- Ruleset effective state: VERIFIED (GitHub API read-back)
- Production readiness: NOT APPLICABLE / BLOCKED (P1 security gates unimplemented; no deployment authorization)
