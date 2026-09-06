from fastapi.testclient import TestClient

from astrobridge.api.app import app


def test_health_endpoint() -> None:
    response = TestClient(app).get("/health", headers={"X-Correlation-ID": "test-correlation"})
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "astrobridge"}
    assert response.headers["X-Correlation-ID"] == "test-correlation"
