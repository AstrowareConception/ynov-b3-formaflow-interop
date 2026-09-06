from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class EvidenceStore:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def _processed_path(self, consumer: str) -> Path:
        return self.root / f"processed-{consumer}.txt"

    def contains(self, consumer: str, event_id: str) -> bool:
        path = self._processed_path(consumer)
        return path.exists() and event_id in path.read_text(encoding="utf-8").splitlines()

    def mark(self, consumer: str, event_id: str) -> None:
        path = self._processed_path(consumer)
        known = set(path.read_text(encoding="utf-8").splitlines()) if path.exists() else set()
        known.add(event_id)
        path.write_text("\n".join(sorted(known)) + "\n", encoding="utf-8", newline="\n")

    def record(self, consumer: str, event: dict[str, Any], outcome: str) -> None:
        trace = {
            "consumer": consumer,
            "eventId": event.get("eventId", "unknown"),
            "correlationId": event.get("correlationId", "unknown"),
            "outcome": outcome,
            "synthetic": True,
        }
        path = self.root / f"evidence-{consumer}.jsonl"
        with path.open("a", encoding="utf-8", newline="\n") as output:
            output.write(json.dumps(trace, sort_keys=True) + "\n")
