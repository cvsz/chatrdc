# chatrdc Startup Guide

This repository has been initialized as the chatrdc product, using the existing governance/tooling baseline without copying over or weakening its controls. Follow these steps for local development and controlled rollout.

## 1. Confirm project identity and branch

- Repository: [cvsz/chatrdc](https://github.com/cvsz/chatrdc)
- Default branch: `main`
- Work on a feature branch and open a pull request.
- Review README.md, ABOUT.md, AGENTS.md, SECURITY.md, CONTRIBUTING.md, ROADMAP.md, and the current branch/head before changing code.
- The template's `scripts/bootstrap.py` is intended for initializing generated repositories. Do not run it against an already initialized product without first reviewing its preview and expected diffs.

## 2. Validate the repository baseline

```bash
make validate-template
```

This validates required repository structure, local Markdown links, and baseline tests. Application checks are defined separately in the Makefile and CI workflow.

## 3. Configure repository administration

The helper is dry-run by default:

```bash
python3 scripts/github_admin.py --repo cvsz/chatrdc
```

Applying repository settings requires explicit authority and an authenticated GitHub identity with Administration permission:

```bash
python3 scripts/github_admin.py --repo cvsz/chatrdc --apply
python3 scripts/github_admin.py --repo cvsz/chatrdc --verify
```

Do not treat the presence of the helper or committed policy files as proof that provider-side controls are active. Verify effective settings by read-back. This project branch does not itself establish that repository settings have been changed or verified.

## 4. Set up local development

Requires Python 3.11+ and Git.

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# Linux/WSL2
source .venv/bin/activate

python -m pip install --upgrade pip
make setup
```

Run the local agent:

```bash
python -m agent
```

Open `http://127.0.0.1:8765/`. In a second terminal, run the stdio MCP server:

```bash
python -m mcp_server.server
```

The MCP server expects the agent at `http://127.0.0.1:8765`. The current API is read-only and local-only.

## 5. Run the project checks

```bash
make lint
make test
make build
make security
make ci
```

Do not remove inherited repository validation, CodeQL, Dependency Review, Dependabot, or other security checks to simplify CI. CI evidence is only valid for the exact commit and checks that actually ran.

## 6. Security and connectivity gates

LAN or Internet remote access is **not implemented and must not be enabled** until all applicable controls in [SECURITY.md](../SECURITY.md) are implemented, tested, and independently reviewed. In particular, do not expose the local agent port directly. The existence of an MCP server is not proof of ChatGPT integration.

## 7. Architecture, release, and operations

Review and keep current:

- [Architecture](architecture.md)
- [Development](development.md)
- [Release and rollback](release.md)
- [Implementation checklist](../IMPLEMENTATION-CHECKLIST.md)
- [Cloudflare/DNS ownership contract](cloudflare-terraform.md)

Public DNS and shared tunnel ingress must remain in the designated infrastructure repository. Do not create duplicate DNS/tunnel ownership here.

## 8. Evidence-based readiness

Record Windows, Linux, and WSL2 results separately. A Linux CI run does not prove Windows acceptance. Before any production release, verify authentication/authorization, remote access, packaging/signing, observability, incident response, rollback, repository controls, and all other applicable release gates. Keep implementation, verification, deployment, and production readiness as separate states.
