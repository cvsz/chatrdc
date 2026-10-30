# Architecture

## Product boundary

chatrdc is a cross-platform desktop-management foundation. The first increment intentionally provides local, read-only diagnostics only. It is not yet a remote desktop transport or a production remote-management service.

## Components

### Local agent

- FastAPI application in `agent/main.py`.
- Health endpoint: `GET /health`.
- Bounded host summary: `GET /api/v1/system`.
- Local dashboard: `GET /`.
- Intended listener: `127.0.0.1:8765`; forwarded-proxy header processing is disabled because the service has no trusted reverse proxy; never expose this port directly to LAN or public ingress.

The host summary includes OS/platform release, Python version, CPU count, and memory/disk capacity. It must not enumerate user documents, environment variables, command lines, or credentials. Agent responses disable caching and set baseline anti-sniffing, anti-framing, referrer, and browser feature-policy headers.

### MCP connector

- `mcp_server/server.py` uses the official Python MCP SDK and stdio transport.
- Tools: `get_agent_health` and `get_system_summary`.
- The connector calls the loopback agent with a short timeout and bounded response size.
- The MCP interface is read-only. No generic shell or file mutation tool is exposed.

### Management UI

The dashboard is served by the local agent and displays health plus the bounded system summary. It is not an authenticated multi-user control plane and must remain local-only.

## Trust boundaries

1. Local operator process → agent listener.
2. MCP host → local stdio connector → loopback agent.
3. Future operator identity/device enrollment → remote gateway → device agent.

The third boundary is **not implemented**. Do not infer remote access from the presence of an MCP server or dashboard.

## Planned layers

1. **P0 — safe local foundation:** bounded read-only API, loopback-only launch path, tests and documentation.
2. **P1 — identity and device enrollment:** revocable device credentials, operator authentication, authorization tests, and audit events.
3. **P1 — secure remote connectivity:** gateway/tunnel integration, TLS, request authentication, rate limits, replay protections, and no direct agent ingress.
4. **P2 — desktop capabilities:** individually allowlisted capabilities with explicit consent and independent security review; do not introduce arbitrary command execution.
5. **P2 — platform packaging:** Windows and Linux/WSL2 install/service workflows, signing/provenance, upgrade and rollback tests.
6. **P3 — ChatGPT integration:** validate the actual supported connector/client registration and end-to-end invocation before claiming integration.

## Deployment and DNS ownership

No deployment or public hostname is configured by this repository. Follow [the Cloudflare/DNS ownership contract](cloudflare-terraform.md); do not create duplicate shared-tunnel or DNS ownership.

## Production boundary

Implementation, tests, deployment, remote access, and production readiness are separate claims. Each requires direct evidence for its exact scope and platform.
