import pytest

from mcp_server.server import _validate_agent_url


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
