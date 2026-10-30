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

Open `http://127.0.0.1:8765/`. The launcher binds to loopback by default. Do not override the listener to a LAN/public interface.

## Run the MCP server

Start the agent in one terminal, then run:

```bash
python -m mcp_server.server
```

This starts a stdio MCP server for a compatible MCP host. ChatGPT integration is not claimed until a supported client configuration and end-to-end invocation have been verified.

## Validation

```bash
make setup
make lint
make test
make build
make security
make ci
```

The lint and format targets cover Python sources under `agent/`, `mcp_server/`, `scripts/`, and `tests/`. For focused development, run `pytest -q tests/test_agent.py tests/test_mcp_config.py` and `ruff check agent mcp_server tests/test_agent.py tests/test_mcp_config.py`.

## Quality and security expectations

- Add tests for behavior and error paths.
- Keep network exposure disabled unless the entire remote-access security gate has passed.
- Preserve read-only capabilities until authorization, audit, consent, and independent review exist.
- Do not commit secrets, tokens, private keys, `.env`, or generated private evidence.
- Keep CI permissions least-privilege and Actions pinned according to the repository policy.
- Fix the root cause of failed validation; do not weaken checks to obtain a green result.

## Platform acceptance

CI runs the Python lint, formatting, test, build, and dependency-audit suite on Linux and Windows runners. Hosted Windows CI is useful compatibility evidence, but it is not equivalent to acceptance on a supported Windows 11 desktop. Record exact OS/build, Python version, dependency versions, commands, results, and failure logs for each platform-specific acceptance run.
