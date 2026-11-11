# Contributing to chatrdc

Contributions should improve the security, correctness, usability, or maintainability of Remote Desktop Commander without bypassing repository controls.

## Development workflow

1. Fork or create a focused feature branch from `main`.
2. Read `AGENTS.md`, `SECURITY.md`, and the relevant architecture docs.
3. Add or update tests for behavior changes.
4. Run the relevant formatting, linting, test, build, and security checks.
5. Update architecture, security, startup, release docs, and `CHANGELOG.md` when relevant.
6. Open a pull request and complete the checklist.

## Branch naming

Use concise prefixes such as `feat/`, `fix/`, `docs/`, `chore/`, `refactor/`, `test/`, or `security/`.

## Commit guidance

Prefer Conventional Commits, for example:

- `feat: add local device diagnostics`
- `fix: reject invalid MCP target URL`
- `security: enforce device-scoped authorization`
- `docs: update deployment guide`

## Pull requests

Pull requests should explain the problem, implementation, tests, security impact, compatibility impact, deployment impact, and rollback plan. Keep changes reviewable. Do not bypass quality or security checks to make a pull request green.

## Security

Do not report exploitable vulnerabilities in public issues. Follow `SECURITY.md`. Do not add remote-control capabilities, arbitrary command execution, file mutation, or public ingress without a reviewed authorization/security design and explicit acceptance criteria.

## Repository validation

Before opening or updating a pull request, run the applicable checks:

```bash
make validate-template
make lint
make test
make build
make security
```

Do not rely on a green result from an older commit after the PR head changes. Required checks must pass on the exact head.

Repository-administration changes require an authenticated admin identity and read-back verification with `scripts/github_admin.py --verify`; configuration intent alone is not evidence.
