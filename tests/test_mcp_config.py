from urllib.request import ProxyHandler
from urllib.request import (
    build_opener as urllib_build_opener,
)

import pytest

from mcp_server import server
from mcp_server.server import _build_local_opener, _validate_agent_url


@pytest.mark.parametrize(
    "url",
    [
        "http://127.0.0.1:8765",
        "http://localhost:8765/",
        "http://[::1]:8765",
    ],
)
def test_accepts_loopback_agent_urls(url):
    assert _validate_agent_url(url).startswith("http://")


@pytest.mark.parametrize(
    "url",
    [
        "https://127.0.0.1:8765",
        "http://example.com:8765",
        "http://192.168.1.20:8765",
        "http://user:password@127.0.0.1:8765",
        "http://127.0.0.1:8765/api/v1/system",
        "http://127.0.0.1:99999",
    ],
)
def test_rejects_non_loopback_or_ambiguous_agent_urls(url):
    with pytest.raises(ValueError):
        _validate_agent_url(url)


def test_local_agent_opener_ignores_environment_proxies(monkeypatch):
    monkeypatch.setenv("HTTP_PROXY", "http://proxy.example:8080")
    monkeypatch.setenv("http_proxy", "http://proxy.example:8080")

    captured_handlers = []

    def recording_build_opener(*handlers):
        captured_handlers.extend(handlers)
        return urllib_build_opener(*handlers)

    monkeypatch.setattr(server, "build_opener", recording_build_opener)

    opener = _build_local_opener()

    proxy_handlers = [
        handler for handler in captured_handlers if isinstance(handler, ProxyHandler)
    ]
    assert len(proxy_handlers) == 1
    assert proxy_handlers[0].proxies == {}
    assert any(handler is server._NoRedirect for handler in captured_handlers)
    assert opener is not None
