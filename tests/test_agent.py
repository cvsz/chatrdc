from fastapi.testclient import TestClient

from agent.main import app

client = TestClient(app, base_url="http://127.0.0.1")


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
