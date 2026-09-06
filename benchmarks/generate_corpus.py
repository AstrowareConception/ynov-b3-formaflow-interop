from __future__ import annotations

import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED = 20260906


def generate(count: int = 1000) -> list[dict[str, object]]:
    randomizer = random.Random(SEED)  # noqa: S311 - deterministic benchmark data only
    events = []
    for index in range(1, count + 1):
        capacity = randomizer.randint(1, 40)
        events.append(
            {
                "eventId": f"10000000-0000-4000-8000-{index:012d}",
                "eventType": "TrainingSessionCreated",
                "version": 1,
                "occurredAt": "2027-01-10T09:00:00Z",
                "correlationId": f"20000000-0000-4000-8000-{index:012d}",
                "causationId": None,
                "producer": "training-management",
                "payload": {
                    "trainingSessionId": f"SES-2027-{index:04d}",
                    "trainingId": f"TRN-{(index % 9999) + 1:04d}",
                    "startsAt": "2027-02-15T08:45:00Z",
                    "endsAt": "2027-02-15T16:45:00Z",
                    "capacity": capacity,
                    "referencePrice": {"amountMinor": 50000 + index, "currency": "EUR"},
                    "status": "SCHEDULED",
                },
            }
        )
    return events


def main() -> None:
    target = ROOT / "benchmarks/corpus/events.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(generate(), indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Generated {target} with seed {SEED}")


if __name__ == "__main__":
    main()
