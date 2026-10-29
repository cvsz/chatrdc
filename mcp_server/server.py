"""Read-only MCP tools that communicate with the loopback agent."""

from __future__ import annotations

import ipaddress
import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from mcp.server.fastmcp import FastMCP

_DEFAULT_AGENT_URL = "http://127.0.0.1:8765"


def _validate_agent_url(value: str) -> str:
    parsed = urlsplit(value)
    if parsed.scheme != "http" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("CHATRDC_AGENT_URL must be an http loopback URL")
    if parsed.path not in {"", "/"} or parsed.query or parsed.fragment:
        raise ValueError("CHATRDC_AGENT_URL must not include a path, query, or fragment")
    host = parsed.hostname.lower()
    if host != "localhost":
        try:
            if not ipaddress.ip_address(host).is_loopback:
                raise ValueError("CHATRDC_AGENT_URL must target loopback")
        except ValueError as exc:
            if "must target loopback" in str(exc):
                raise
            raise ValueError("CHATRDC_AGENT_URL must target loopback") from exc
    try:
        port = parsed.port
    except ValueError as exc:
        raise ValueError("CHATRDC_AGENT_URL has an invalid port") from exc
    if port is not None and not 1 <= port <= 65535:
        raise ValueError("CHATRDC_AGENT_URL has an invalid port")
    return value.rstrip("/")


AGENT_URL = _validate_agent_url(os.environ.get("CHATRDC_AGENT_URL", _DEFAULT_AGENT_URL))
mcp = FastMCP("Remote Desktop Commander")


def _get_json(path: str) -> dict:
    if path not in {"/health", "/api/v1/system"}:
        raise ValueError("Unsupported agent path")
    req = Request(f"{AGENT_URL}{path}", headers={"Accept": "application/json"})
    try:
        with urlopen(req, timeout=3.0) as response:
            if response.status != 200:
                raise RuntimeError("Agent returned an unexpected status")
            data = json.loads(response.read(256_000).decode("utf-8"))
            if not isinstance(data, dict):
                raise RuntimeError("Agent returned invalid data")
            return data
    except (HTTPError, URLError, TimeoutError, ValueError) as exc:
        raise RuntimeError("Local agent unavailable or returned invalid data") from exc


@mcp.tool()
def get_agent_health() -> dict:
    """Check whether the local agent is responding."""
    return _get_json("/health")


@mcp.tool()
def get_system_summary() -> dict:
    """Read basic OS, CPU, memory, and disk capacity without accessing user documents."""
    return _get_json("/api/v1/system")


if __name__ == "__main__":
    mcp.run(transport="stdio")
