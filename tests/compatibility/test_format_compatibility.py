import io
import json
from pathlib import Path

from fastavro import parse_schema, schemaless_reader, schemaless_writer

from generated.training_session_created_v1_pb2 import TrainingSessionCreatedV1
from generated.training_session_created_v2_pb2 import TrainingSessionCreatedV2

ROOT = Path(__file__).resolve().parents[2]


def schema(version: int) -> dict:
    path = ROOT / f"contracts/avro/training-session-created.v{version}.avsc"
    return parse_schema(json.loads(path.read_text(encoding="utf-8")))


def test_protobuf_old_reader_ignores_and_preserves_unknown_fields() -> None:
    event = json.loads(
        (ROOT / "contracts/examples/training-session-created.v2.valid.json").read_text()
    )
    current = TrainingSessionCreatedV2(
        event_id=event["eventId"], event_type=event["eventType"], version=2,
        occurred_at=event["occurredAt"], correlation_id=event["correlationId"],
        producer=event["producer"],
    )
    payload = event["payload"]
    current.payload.training_session_id = payload["trainingSessionId"]
    current.payload.training_id = payload["trainingId"]
    current.payload.starts_at = payload["startsAt"]
    current.payload.ends_at = payload["endsAt"]
    current.payload.capacity = payload["capacity"]
    current.payload.reference_price.amount_minor = payload["referencePrice"]["amountMinor"]
    current.payload.reference_price.currency = "EUR"
    current.payload.status = "SCHEDULED"
    current.payload.delivery_mode = payload["deliveryMode"]
    current.payload.location_label = payload["location"]["label"]
    old = TrainingSessionCreatedV1.FromString(current.SerializeToString())
    restored = TrainingSessionCreatedV2.FromString(old.SerializeToString())
    assert restored.payload.delivery_mode == "HYBRID"
    assert restored.payload.location_label == "Synthetic Campus A / Local Room"


def test_avro_v1_writer_to_v2_reader_applies_defaults() -> None:
    event = json.loads(
        (ROOT / "contracts/examples/training-session-created.v1.valid.json").read_text()
    )
    output = io.BytesIO()
    schemaless_writer(output, schema(1), event)
    restored = schemaless_reader(io.BytesIO(output.getvalue()), schema(1), schema(2))
    assert restored["payload"]["deliveryMode"] == "ONSITE"
    assert restored["payload"]["location"]["label"] == "TO_BE_CONFIRMED"


def test_avro_v2_writer_to_v1_reader_discards_additive_fields() -> None:
    event = json.loads(
        (ROOT / "contracts/examples/training-session-created.v2.valid.json").read_text()
    )
    output = io.BytesIO()
    schemaless_writer(output, schema(2), event)
    restored = schemaless_reader(io.BytesIO(output.getvalue()), schema(2), schema(1))
    assert "deliveryMode" not in restored["payload"]


def test_json_strict_v1_needs_an_adapter_for_v2() -> None:
    from astrobridge.contracts.validation import validate_event

    event = json.loads(
        (ROOT / "contracts/examples/training-session-created.v2.valid.json").read_text()
    )
    assert validate_event(event, version=1)
