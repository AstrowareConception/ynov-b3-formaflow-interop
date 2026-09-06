from __future__ import annotations

import json
from pathlib import Path

import httpx

from astrobridge.config import Settings
from astrobridge.messaging.consumer import consume_once
from astrobridge.messaging.publisher import publish_event

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    response = httpx.get("http://127.0.0.1:8000/health", timeout=5)
    response.raise_for_status()
    event = json.loads(
        (ROOT / "fixtures/valid/training-session-created.v1.json").read_text(encoding="utf-8")
    )
    settings = Settings()
    if not publish_event(event, settings):
        raise RuntimeError("publisher confirm was not received")
    consumers = ("administration", "notification")
    first = {consumer: consume_once(consumer, settings) for consumer in consumers}
    publish_event(event, settings)
    second = {consumer: consume_once(consumer, settings) for consumer in consumers}
    if set(first.values()) != {"processed"} or set(second.values()) != {"duplicate"}:
        raise RuntimeError(f"unexpected effects: first={first}, duplicate={second}")
    for consumer in ("administration", "notification"):
        evidence = settings.data_dir / f"evidence-{consumer}.jsonl"
        if not evidence.exists():
            raise RuntimeError(f"missing local evidence: {evidence}")
    print("Smoke passed: API, contract, confirmed publish, two consumers, duplicate and evidence")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
