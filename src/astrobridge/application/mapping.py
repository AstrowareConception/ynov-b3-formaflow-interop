from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any
from uuid import UUID


@dataclass(frozen=True)
class InternalTrainingSession:
    """Source-side shape; deliberately different from the public contract."""

    session_code: str
    course_code: str
    begins_at: datetime
    finishes_at: datetime
    seat_limit: int
    price_cents: int
    currency_code: str = "EUR"
    lifecycle: str = "planned"


def _utc(value: datetime) -> str:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("source timestamps must be timezone-aware")
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def to_integration_event(
    source: InternalTrainingSession,
    *,
    event_id: UUID,
    occurred_at: datetime,
    correlation_id: UUID,
    causation_id: UUID | None = None,
) -> dict[str, Any]:
    """Map source semantics to the stable public envelope without leaking source fields."""
    if source.lifecycle != "planned":
        raise ValueError("only a newly planned session can produce TrainingSessionCreated")
    return {
        "eventId": str(event_id),
        "eventType": "TrainingSessionCreated",
        "version": 1,
        "occurredAt": _utc(occurred_at),
        "correlationId": str(correlation_id),
        "causationId": str(causation_id) if causation_id else None,
        "producer": "training-management",
        "payload": {
            "trainingSessionId": source.session_code,
            "trainingId": source.course_code,
            "startsAt": _utc(source.begins_at),
            "endsAt": _utc(source.finishes_at),
            "capacity": source.seat_limit,
            "referencePrice": {
                "amountMinor": source.price_cents,
                "currency": source.currency_code,
            },
            "status": "SCHEDULED",
        },
    }
