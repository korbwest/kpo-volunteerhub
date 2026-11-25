def test_health_http(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_response_is_not_cached(client):
    response = client.get("/api/health")
    assert response.headers["Cache-Control"] == "no-store"
