import json
import time
from pathlib import Path

from fastapi.testclient import TestClient

from astrobridge.api.app import app
from astrobridge.webhooks.security import signature


def test_local_webhook_accepts_once_then_rejects_replay() -> None:
    root = Path(__file__).resolve().parents[2]
    event = json.loads(
        (root / "fixtures/valid/training-session-created.v1.json").read_text(encoding="utf-8")
    )
    body = json.dumps(event, separators=(",", ":"), sort_keys=True).encode()
    timestamp = int(time.time())
    key = f"receiver-{timestamp}"
    demo_value = "synthetic_demo_secret_change_me"
    headers = {
        "X-AstroBridge-Timestamp": str(timestamp),
        "X-AstroBridge-Idempotency-Key": key,
        "X-AstroBridge-Signature": signature(demo_value, timestamp, key, body),
        "Content-Type": "application/json",
    }
    client = TestClient(app)
    first = client.post("/webhooks/training-session", content=body, headers=headers)
    replay = client.post("/webhooks/training-session", content=body, headers=headers)
    assert first.status_code == 200
    assert replay.status_code == 401


def test_signed_json_array_is_rejected_as_a_contract_error() -> None:
    body = b"[]"
    timestamp = int(time.time())
    key = f"non-object-{timestamp}"
    demo_value = "synthetic_demo_secret_change_me"
    headers = {
        "X-AstroBridge-Timestamp": str(timestamp),
        "X-AstroBridge-Idempotency-Key": key,
        "X-AstroBridge-Signature": signature(demo_value, timestamp, key, body),
        "Content-Type": "application/json",
    }
    response = TestClient(app).post("/webhooks/training-session", content=body, headers=headers)
    assert response.status_code == 422
    assert response.json()["error"] == "contract_validation_failed"
    assert "$: expected a JSON object (rule: type)" in response.json()["message"]
