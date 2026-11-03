"""Live connectivity tests for the dashboard, agent API, and MCP connector."""

from __future__ import annotations

import socket
import threading
import time
from collections.abc import Iterator

import pytest
import uvicorn

from agent.main import app
from mcp_server import server as mcp_server


@pytest.fixture
def live_agent(monkeypatch: pytest.MonkeyPatch) -> Iterator[str]:
    """Run the real ASGI app on an ephemeral loopback TCP port."""
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]

    base_url = f"http://127.0.0.1:{port}"
    config = uvicorn.Config(
        app,
        host="127.0.0.1",
        port=port,
        log_level="critical",
        access_log=False,
        proxy_headers=False,
    )
    instance = uvicorn.Server(config)
    thread = threading.Thread(target=instance.run, daemon=True)
    thread.start()

    deadline = time.monotonic() + 5
    while not instance.started and thread.is_alive() and time.monotonic() < deadline:
        time.sleep(0.01)

    if not instance.started:
        instance.should_exit = True
        thread.join(timeout=2)
        pytest.fail("Local agent did not start listening within 5 seconds")

    monkeypatch.setattr(mcp_server, "AGENT_URL", base_url)
    try:
        yield base_url
    finally:
        instance.should_exit = True
        thread.join(timeout=5)
        assert not thread.is_alive(), "Local agent did not shut down cleanly"


def test_dashboard_and_agent_api_are_reachable_over_loopback(live_agent: str) -> None:
    from urllib.request import urlopen

    with urlopen(f"{live_agent}/", timeout=2) as response:
        dashboard = response.read().decode("utf-8")
        assert response.status == 200
    assert "fetch('/health')" in dashboard
    assert "fetch('/api/v1/system')" in dashboard

    with urlopen(f"{live_agent}/health", timeout=2) as response:
        health = response.read().decode("utf-8")
        assert response.status == 200
    assert '"status":"ok"' in health


def test_mcp_connector_reads_live_agent_health(live_agent: str) -> None:
    result = mcp_server.get_agent_health()

    assert result["status"] == "ok"
    assert result["service"] == "chatrdc-agent"


def test_mcp_connector_reads_live_system_summary(live_agent: str) -> None:
    result = mcp_server.get_system_summary()

    assert result["hostname"]
    assert result["platform"]
    assert result["cpu_count"] >= 1
    assert result["memory_total_bytes"] > 0
    assert "environment" not in result
    assert "home_directory" not in result


def test_mcp_connector_reports_agent_disconnected(monkeypatch: pytest.MonkeyPatch) -> None:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        unused_port = probe.getsockname()[1]

    monkeypatch.setattr(mcp_server, "AGENT_URL", f"http://127.0.0.1:{unused_port}")

    with pytest.raises(RuntimeError, match="Local agent unavailable"):
        mcp_server.get_agent_health()
