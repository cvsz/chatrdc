# ADR 0001: Local-only first increment

- Status: Accepted
- Date: 2026-10-30

## Context

Remote desktop management crosses a high-risk trust boundary. Exposing a desktop agent before identity, authorization, audit, revocation, and transport security exist could permit unauthorized access to a user's device.

## Decision

The first increment is local-only and read-only. The agent launch path binds to loopback. The MCP server exposes only health and a bounded system summary. The agent rejects non-loopback Host values and mismatched browser Origin values. The MCP connector only accepts a loopback HTTP agent URL.

LAN/Internet remote access and state-changing desktop capabilities remain disabled until separate design, implementation, negative tests, and independent review pass.

## Consequences

- The first increment can be tested without public ingress or cloud infrastructure.
- The system cannot yet manage devices remotely.
- MCP server presence does not establish ChatGPT integration.
- A loopback bind alone is not a complete security boundary; Host/Origin checks, OS access control, dependency updates, and platform testing remain necessary.
- Future remote connectivity must use a reviewed gateway/tunnel and must never expose the agent port directly.

## Revisit when

A threat model, operator/device identity model, authorization contract, audit/revocation design, and platform acceptance plan are ready for independent review.
