# Release

## Current release status

chatrdc is an implementation scaffold. No production release, signed installer, public endpoint, or remote-access capability is claimed.

## Release gates

1. Confirm the exact release commit and required GitHub checks.
2. Verify repository administration controls by provider read-back.
3. Pass lint, tests, build, dependency/security checks, and platform-specific acceptance.
4. Review the threat model, authentication/authorization, audit, data exposure, and dependency supply chain.
5. Verify Windows and Linux/WSL2 packaging and clean-install/upgrade behavior.
6. Sign installers and establish artifact provenance before distributing binaries.
7. Verify configuration, key rotation, incident response, backup/recovery, and rollback where applicable.
8. Publish only through a trusted, protected release workflow.
9. Verify the published artifact and installation on a clean target environment.
10. Record residual risks separately; accepted risk does not convert an unverified gate into a verified one.

## Remote-access gate

Do not enable LAN or Internet access until the mandatory controls in [SECURITY.md](../SECURITY.md) are implemented, tested, and independently reviewed. The local agent port must never be exposed directly.

## Rollback

Document and test, as appropriate:

- last known-good artifact and version
- application/configuration rollback
- credential/device revocation after compromise
- removal of exposed ingress/routes
- operator and stakeholder communication

A written rollback plan without environment-appropriate execution evidence is not proof that recovery works.
