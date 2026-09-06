from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="AstroBridge", version="1.0.0")


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
    return JSONResponse({"status": "ready", "stage": "course-start"})

