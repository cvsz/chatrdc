# chatrdc — Remote Desktop Commander

Security-first desktop management foundation for Windows and Linux/WSL2, built around an MCP connector, a loopback-only local agent, and a local management UI.

## Status

**Development scaffold; not production-ready.** The first increment provides read-only host diagnostics, a local dashboard, and two MCP tools. Authenticated device enrollment, remote gateway, remote desktop streaming/control, installers/signing, and verified ChatGPT integration are not implemented.

## Product scope

- **MCP connector:** stdio MCP server for safe, read-only diagnostics.
- **Local agent:** FastAPI service bound to loopback by default.
- **Management UI:** local status dashboard; no remote administration in this increment.
- **Platforms:** Windows and Linux/WSL2 as the v1 target; verify each platform before claiming support.
- **Connectivity:** local-only first. LAN and secure Internet access remain gated on authentication, authorization, TLS/gateway, audit, and security verification.

## Quick start

Requires Python 3.11+.

Install the project and its development dependencies:

```bash
python -m pip install -e ".[dev]"
```

Start the local agent in terminal 1:

```bash
python -m agent
```

Open http://127.0.0.1:8765/ in a browser. The dashboard and API are served by the same agent process and origin.

Start the MCP stdio connector in terminal 2 (or configure the command in a compatible MCP host):

```bash
python -m mcp_server.server
```

The MCP connector calls the same local agent at `http://127.0.0.1:8765`. The agent must be running before MCP tools can return live data. If the agent is stopped, MCP reports the agent as unavailable; restart the agent to restore connectivity.

Do not expose the agent directly to a LAN or the Internet.

## Connectivity verification

The live connectivity suite starts the real ASGI agent on an ephemeral loopback TCP port and verifies dashboard/API reachability, MCP health and system-summary calls, and the disconnected-agent error path:

```bash
python -m pytest -q tests/test_connectivity.py
```

Run the complete development checks with:

```bash
make setup
make lint
make test
make build
make security
make ci
```

## Architecture and policy

- [Architecture](docs/architecture.md)
- [Development](docs/development.md)
- [Security model and release gates](SECURITY.md)
- [Release and rollback](docs/release.md)
- [Implementation checklist](IMPLEMENTATION-CHECKLIST.md)
- [Startup guide](docs/startup.md)
- [Cloudflare/DNS ownership contract](docs/cloudflare-terraform.md)

## Security boundary

No arbitrary shell execution, file mutation, process termination, service control, screen capture, or remote-control tools are exposed in the current scaffold. Remote access must not be enabled until the required controls and tests in [SECURITY.md](SECURITY.md) are implemented and independently reviewed.

## License

See [LICENSE](LICENSE). Preserve the repository's existing license and attribution terms.
