from datetime import UTC, datetime
from uuid import UUID

from astrobridge.application.mapping import InternalTrainingSession, to_integration_event


def test_mapping_hides_internal_names_and_normalizes_units() -> None:
    source = InternalTrainingSession(
        session_code="SES-2027-0001",
        course_code="TRN-0001",
        begins_at=datetime(2027, 2, 15, 9, 45, tzinfo=UTC),
        finishes_at=datetime(2027, 2, 15, 17, 45, tzinfo=UTC),
        seat_limit=12,
        price_cents=69000,
    )
    event = to_integration_event(
        source,
        event_id=UUID("10000000-0000-4000-8000-000000000001"),
        occurred_at=datetime(2027, 1, 10, 9, tzinfo=UTC),
        correlation_id=UUID("20000000-0000-4000-8000-000000000001"),
    )
    assert event["eventType"] == "TrainingSessionCreated"
    assert event["payload"]["referencePrice"]["amountMinor"] == 69000
    assert not ({"seat_limit", "price_cents", "lifecycle"} & event["payload"].keys())
