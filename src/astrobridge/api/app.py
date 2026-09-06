from __future__ import annotations

import json
from typing import Any

from fastapi import FastAPI, HTTPException, Query, Request, Response
from fastapi.responses import JSONResponse

from astrobridge.config import Settings
from astrobridge.contracts.adapters import downcast_v2_to_v1
from astrobridge.contracts.validation import assert_valid_event
from astrobridge.messaging.publisher import publish_event
from astrobridge.observability.store import EvidenceStore
from astrobridge.webhooks.security import ReplayGuard

app = FastAPI(title="AstroBridge", version="1.0.0")
webhook_guard = ReplayGuard()


@app.middleware("http")
async def correlation_header(request: Request, call_next):  # type: ignore[no-untyped-def]
    correlation_id = request.headers.get("X-Correlation-ID", "synthetic-local-request")
    response = await call_next(request)
    response.headers["X-Correlation-ID"] = correlation_id
    return response


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "astrobridge"}


@app.get("/ready")
def ready() -> JSONResponse:
    return JSONResponse({"status": "ready", "stage": "checkpoint-versioning"})


@app.exception_handler(ValueError)
async def contract_error_handler(request: Request, error: ValueError) -> JSONResponse:
    correlation_id = request.headers.get("X-Correlation-ID", "synthetic-local-request")
    return JSONResponse(
        status_code=422,
        content={
            "error": "contract_validation_failed",
            "message": str(error),
            "correlationId": correlation_id,
        },
    )


@app.post("/api/v1/events")
def accept_v1_event(
    event: dict[str, Any], response: Response, publish: bool = Query(default=False)
) -> dict[str, Any]:
    assert_valid_event(event, version=1)
    if publish:
        publish_event(event)
    response.headers["Deprecation"] = "true"
    response.headers["Sunset"] = "Thu, 30 Sep 2027 23:59:59 GMT"
    response.headers["Link"] = '</docs/versioning.md>; rel="deprecation"'
    return {"accepted": True, "version": 1, "event": event}


@app.post("/api/v2/events")
def accept_v2_event(event: dict[str, Any], publish: bool = Query(default=False)) -> dict[str, Any]:
    assert_valid_event(event, version=2)
    legacy = downcast_v2_to_v1(event)
    assert_valid_event(legacy, version=1)
    if publish:
        publish_event(legacy)
    return {"accepted": True, "version": 2, "legacyV1": legacy}


@app.get("/evidence/{consumer}")
def read_evidence(consumer: str) -> dict[str, object]:
    if consumer not in {"administration", "notification", "webhook"}:
        raise HTTPException(status_code=404, detail="unknown synthetic consumer")
    path = Settings().data_dir / f"evidence-{consumer}.jsonl"
    lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    return {"consumer": consumer, "synthetic": True, "traces": [json.loads(line) for line in lines]}


@app.post("/webhooks/training-session")
async def receive_training_session_webhook(request: Request) -> dict[str, object]:
    body = await request.body()
    try:
        timestamp = int(request.headers["X-AstroBridge-Timestamp"])
        key = request.headers["X-AstroBridge-Idempotency-Key"]
        supplied = request.headers["X-AstroBridge-Signature"]
    except (KeyError, ValueError) as error:
        raise HTTPException(status_code=400, detail="missing or invalid webhook headers") from error
    if not webhook_guard.verify(Settings().webhook_secret, timestamp, key, body, supplied):
        raise HTTPException(status_code=401, detail="invalid signature or replay")
    event = json.loads(body)
    assert_valid_event(event)
    EvidenceStore(Settings().data_dir).record("webhook", event, "accepted")
    return {"accepted": True, "idempotencyKey": key}
