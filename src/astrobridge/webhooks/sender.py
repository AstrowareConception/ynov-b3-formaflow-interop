from __future__ import annotations

import asyncio
import json
import time
from collections.abc import Awaitable, Callable
from typing import Any

import httpx

from astrobridge.webhooks.security import signature


async def send_webhook(
    url: str,
    event: dict[str, Any],
    secret: str,
    *,
    attempts: int = 3,
    timeout: float = 2.0,
    transport: httpx.AsyncBaseTransport | None = None,
    sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
) -> httpx.Response:
    if attempts <= 0:
        raise RuntimeError("webhook attempts must be positive")
    body = json.dumps(event, separators=(",", ":"), sort_keys=True).encode()
    timestamp = int(time.time())
    key = str(event["eventId"])
    headers = {
        "Content-Type": "application/json",
        "X-AstroBridge-Timestamp": str(timestamp),
        "X-AstroBridge-Idempotency-Key": key,
        "X-AstroBridge-Signature": signature(secret, timestamp, key, body),
    }
    last_error: httpx.HTTPError | None = None
    async with httpx.AsyncClient(timeout=timeout, transport=transport) as client:
        for attempt in range(attempts):
            try:
                response = await client.post(url, content=body, headers=headers)
                response.raise_for_status()
                return response
            except httpx.HTTPError as error:
                last_error = error
                if attempt + 1 < attempts:
                    await sleep(0.1 * (attempt + 1))
    assert last_error is not None
    raise last_error
