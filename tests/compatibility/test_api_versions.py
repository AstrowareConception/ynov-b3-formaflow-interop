import json
from pathlib import Path

from fastapi.testclient import TestClient

from astrobridge.api.app import app

ROOT = Path(__file__).resolve().parents[2]
CLIENT = TestClient(app)


def event(version: int) -> dict:
    path = ROOT / f"contracts/examples/training-session-created.v{version}.valid.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_old_v1_client_with_v1_route() -> None:
    response = CLIENT.post("/api/v1/events", json=event(1))
    assert response.status_code == 200
    assert response.json()["event"]["version"] == 1
    assert response.headers["Deprecation"] == "true"
    assert "Sunset" in response.headers


def test_old_v1_client_still_works_after_v2_introduction() -> None:
    assert CLIENT.post("/api/v2/events", json=event(2)).status_code == 200
    response = CLIENT.post("/api/v1/events", json=event(1))
    assert response.status_code == 200


def test_v2_route_exposes_valid_legacy_downcast() -> None:
    response = CLIENT.post("/api/v2/events", json=event(2))
    assert response.status_code == 200
    assert response.json()["legacyV1"]["version"] == 1


def test_incompatible_type_is_rejected_with_normalized_error() -> None:
    invalid = json.loads((ROOT / "fixtures/invalid/v2-capacity-type.json").read_text())
    response = CLIENT.post(
        "/api/v2/events", json=invalid, headers={"X-Correlation-ID": "compat-test"}
    )
    assert response.status_code == 422
    assert response.json()["correlationId"] == "compat-test"
    assert "$.payload.capacity" in response.json()["message"]
