import json
from pathlib import Path

import httpx
import pytest

from astrobridge.webhooks.sender import send_webhook

ROOT = Path(__file__).resolve().parents[2]
EVENT = json.loads(
    (ROOT / "fixtures/valid/training-session-created.v1.json").read_text(encoding="utf-8")
)


@pytest.mark.asyncio
async def test_webhook_retries_after_5xx_then_succeeds_without_real_wait() -> None:
    statuses = iter([503, 202])
    requests: list[httpx.Request] = []
    delays: list[float] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(next(statuses), request=request)

    async def record_sleep(delay: float) -> None:
        delays.append(delay)

    response = await send_webhook(
        "https://webhook.example.test/training-session",
        EVENT,
        "synthetic_demo_secret_change_me",
        transport=httpx.MockTransport(handler),
        sleep=record_sleep,
    )

    assert response.status_code == 202
    assert len(requests) == 2
    assert delays == [0.1]


@pytest.mark.asyncio
async def test_webhook_5xx_retries_are_bounded() -> None:
    calls = 0
    delays: list[float] = []

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(503, request=request)

    async def record_sleep(delay: float) -> None:
        delays.append(delay)

    with pytest.raises(httpx.HTTPStatusError):
        await send_webhook(
            "https://webhook.example.test/training-session",
            EVENT,
            "synthetic_demo_secret_change_me",
            attempts=3,
            transport=httpx.MockTransport(handler),
            sleep=record_sleep,
        )

    assert calls == 3
    assert delays == [0.1, 0.2]
