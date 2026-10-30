from fastapi.testclient import TestClient

from agent.main import app

client = TestClient(
    app,
    base_url="http://127.0.0.1",
    client=("127.0.0.1", 50000),
)


def test_health_is_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_system_summary_is_bounded():
    response = client.get("/api/v1/system")
    assert response.status_code == 200
    body = response.json()
    assert body["platform"]
    assert body["cpu_count"] >= 1
    assert body["memory_total_bytes"] > 0
    assert "environment" not in body
    assert "home_directory" not in body


def test_dashboard_serves_local_ui():
    response = client.get("/")
    assert response.status_code == 200
    assert "Remote Desktop Commander" in response.text
    assert "Read-only preview" in response.text


def test_rejects_untrusted_host_header():
    response = client.get("/health", headers={"host": "attacker.example"})
    assert response.status_code == 403


def test_rejects_cross_origin_browser_request():
    response = client.get(
        "/api/v1/system",
        headers={"origin": "http://attacker.example"},
    )
    assert response.status_code == 403


def test_rejects_origin_with_mismatched_scheme():
    response = client.get("/health", headers={"origin": "https://127.0.0.1:80"})
    assert response.status_code == 403


def test_rejects_origin_with_userinfo():
    response = client.get("/health", headers={"origin": "http://user@127.0.0.1"})
    assert response.status_code == 403


def test_rejects_non_loopback_peer():
    remote_client = TestClient(
        app,
        base_url="http://127.0.0.1",
        client=("192.168.1.20", 12345),
    )

    response = remote_client.get("/health")

    assert response.status_code == 403
    assert response.json()["detail"] == "Local connections only"


def test_rejects_missing_peer():
    missing_peer_client = TestClient(
        app,
        base_url="http://127.0.0.1",
        client=None,
    )

    response = missing_peer_client.get("/health")

    assert response.status_code == 403


def test_forwarded_loopback_header_does_not_override_remote_peer():
    remote_client = TestClient(
        app,
        base_url="http://127.0.0.1",
        client=("192.168.1.20", 12345),
    )

    response = remote_client.get(
        "/health",
        headers={
            "x-forwarded-for": "127.0.0.1",
            "forwarded": "for=127.0.0.1",
        },
    )

    assert response.status_code == 403


def test_accepts_ipv4_mapped_ipv6_loopback_peer():
    mapped_client = TestClient(
        app,
        base_url="http://127.0.0.1",
        client=("::ffff:127.0.0.1", 12345),
    )

    response = mapped_client.get("/health")

    assert response.status_code == 200
