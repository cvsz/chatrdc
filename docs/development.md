# Development

## Requirements

- Python 3.11 or newer.
- Git.
- A supported Windows or Linux/WSL2 environment for platform-specific acceptance.
- Network access to install dependencies from the configured package index.

## Local setup

```bash
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Linux/WSL2:
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Run the local agent

```bash
python -m agent
```

Open `http://127.0.0.1:8765/`. The launcher binds to loopback by default. Forwarded proxy headers are disabled; the service must not be exposed to a LAN/public interface.

## Run the MCP server

Start the agent in one terminal, then run in another terminal or configure it as a stdio MCP server in a compatible MCP host:

```bash
python -m mcp_server.server
```

The MCP connector calls the agent at `http://127.0.0.1:8765`. If the agent is stopped, MCP health and system-summary tools return an unavailable error. Start the agent first and restart it if connectivity is lost. ChatGPT integration is not claimed until a supported client configuration and end-to-end invocation have been verified.

## Live connectivity tests

```bash
python -m pytest -q tests/test_connectivity.py
```

These tests start the real ASGI app on an ephemeral loopback TCP port and verify:
- The dashboard and HTTP health endpoint are reachable.
- MCP health and system-summary tools retrieve live data from that agent.
- MCP reports a clear unavailable error when the agent is not listening.

## Validation

```bash
make setup
make lint
make test
make build
make security
make ci
```

For focused development, run `pytest -q tests/test_agent.py tests/test_mcp_config.py tests/test_connectivity.py` and `ruff check agent mcp_server tests/test_agent.py tests/test_mcp_config.py tests/test_connectivity.py`.

## Quality and security expectations

- Add tests for behavior and error paths.
- Keep network exposure disabled unless the entire remote-access security gate has passed.
- Preserve read-only capabilities until authorization, audit, consent, and independent review exist.
- Do not commit secrets, tokens, private keys, `.env`, or generated private evidence.
- Keep CI permissions least-privilege and Actions pinned according to the repository policy.
- Fix the root cause of failed validation; do not weaken checks to obtain a green result.

## Platform acceptance

Linux CI is not evidence of Windows acceptance. Record exact OS/build, Python version, dependency versions, commands, results, and failure logs for each platform-specific test run.
