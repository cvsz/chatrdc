"""Read-only MCP tools that communicate with the loopback agent."""

from __future__ import annotations

import ipaddress
import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, ProxyHandler, Request, build_opener

from mcp.server import MCPServer

_DEFAULT_AGENT_URL = "http://127.0.0.1:8765"


def _validate_agent_url(value: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError("CHATRDC_AGENT_URL must be an http loopback URL")

    if any(char.isspace() or ord(char) < 0x20 or ord(char) == 0x7F for char in value):
        raise ValueError("CHATRDC_AGENT_URL contains invalid characters")
    if "\\" in value or "?" in value or "#" in value:
        raise ValueError("CHATRDC_AGENT_URL must not contain ambiguous URL syntax")

    try:
        parsed = urlsplit(value)
        if (
            parsed.scheme.lower() != "http"
            or not parsed.netloc
            or not parsed.hostname
            or parsed.username is not None
            or parsed.password is not None
        ):
            raise ValueError("CHATRDC_AGENT_URL must be an http loopback URL")

        if parsed.path not in {"", "/"} or parsed.query or parsed.fragment:
            raise ValueError("CHATRDC_AGENT_URL must not include a path, query, or fragment")

        address = ipaddress.ip_address(parsed.hostname)
        port = parsed.port
    except ValueError as exc:
        raise ValueError(
            "CHATRDC_AGENT_URL must contain a valid loopback IP literal and port"
        ) from exc

    if not address.is_loopback:
        raise ValueError("CHATRDC_AGENT_URL must target loopback")

    if port is not None and not 1 <= port <= 65535:
        raise ValueError("CHATRDC_AGENT_URL has an invalid port")

    return value.rstrip("/")


AGENT_URL = _validate_agent_url(os.environ.get("CHATRDC_AGENT_URL", _DEFAULT_AGENT_URL))
mcp = MCPServer("Remote Desktop Commander")


class _NoRedirect(HTTPRedirectHandler):
    """Do not let a local agent response redirect the MCP client off-loopback."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _build_local_opener():
    """Ignore ambient proxy variables for the loopback-only agent connection."""
    return build_opener(ProxyHandler({}), _NoRedirect)


def _get_json(path: str) -> dict:
    if path not in {"/health", "/api/v1/system"}:
        raise ValueError("Unsupported agent path")
    req = Request(f"{AGENT_URL}{path}", headers={"Accept": "application/json"})
    try:
        with _build_local_opener().open(req, timeout=3.0) as response:
            if response.status != 200:
                raise RuntimeError("Agent returned an unexpected status")
            data = json.loads(response.read(256_000).decode("utf-8"))
            if not isinstance(data, dict):
                raise TypeError("Agent returned invalid data")
            return data
    except (HTTPError, URLError, TimeoutError, TypeError, ValueError) as exc:
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
