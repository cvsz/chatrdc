import pytest
from fastapi.testclient import TestClient

from agent import main
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


def test_system_summary_hides_internal_error_details(monkeypatch):
    def fail_summary():
        raise RuntimeError("sensitive internal diagnostic")

    monkeypatch.setattr(main, "_summary", fail_summary)
    response = client.get("/api/v1/system")

    assert response.status_code == 500
    assert response.json() == {"detail": "Unable to collect system summary"}
    assert "sensitive internal diagnostic" not in response.text


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


def test_accepts_matching_loopback_origin():
    response = client.get("/health", headers={"origin": "http://127.0.0.1"})
    assert response.status_code == 200


@pytest.mark.parametrize(
    "origin",
    [
        "https://127.0.0.1:80",
        "http://localhost",
        "http://127.0.0.1:8080",
        "http://127.0.0.1/path",
        "http://127.0.0.1/?query=1",
        "http://127.0.0.1/#fragment",
        "http://user@127.0.0.1",
        "null",
        "http://127.0.0.1:invalid",
    ],
)
def test_rejects_malformed_or_mismatched_origins(origin):
    response = client.get("/health", headers={"origin": origin})
    assert response.status_code == 403


def test_agent_sets_baseline_security_headers():
    response = client.get("/api/v1/system")

    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"
    assert response.headers["referrer-policy"] == "no-referrer"
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["permissions-policy"] == (
        "camera=(), microphone=(), geolocation=()"
    )


def test_rejected_host_response_also_has_security_headers():
    response = client.get("/health", headers={"host": "attacker.example"})

    assert response.status_code == 403
    assert response.headers["cache-control"] == "no-store"
    assert response.headers["x-content-type-options"] == "nosniff"

