from fastapi.testclient import TestClient

from app.main import app, health


def test_health_status():
    assert health() == {"status": "ok"}


def test_health_http():
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
