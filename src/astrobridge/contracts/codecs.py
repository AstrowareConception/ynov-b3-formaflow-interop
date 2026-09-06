from __future__ import annotations

import io
import json
from pathlib import Path
from typing import Any, cast

from fastavro import parse_schema, schemaless_reader, schemaless_writer

from generated.training_session_created_v1_pb2 import (  # type: ignore[attr-defined]
    TrainingSessionCreatedV1,
)

ROOT = Path(__file__).resolve().parents[3]


def encode_json(event: dict[str, Any]) -> bytes:
    return json.dumps(event, separators=(",", ":"), sort_keys=True).encode()


def decode_json(data: bytes) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(data))


def to_proto(event: dict[str, Any]) -> TrainingSessionCreatedV1:
    payload = event["payload"]
    message = TrainingSessionCreatedV1(
        event_id=event["eventId"],
        event_type=event["eventType"],
        version=event["version"],
        occurred_at=event["occurredAt"],
        correlation_id=event["correlationId"],
        producer=event["producer"],
    )
    if event["causationId"] is not None:
        message.causation_id = event["causationId"]
    message.payload.training_session_id = payload["trainingSessionId"]
    message.payload.training_id = payload["trainingId"]
    message.payload.starts_at = payload["startsAt"]
    message.payload.ends_at = payload["endsAt"]
    message.payload.capacity = payload["capacity"]
    message.payload.reference_price.amount_minor = payload["referencePrice"]["amountMinor"]
    message.payload.reference_price.currency = payload["referencePrice"]["currency"]
    message.payload.status = payload["status"]
    return message


def from_proto(message: TrainingSessionCreatedV1) -> dict[str, Any]:
    return {
        "eventId": message.event_id,
        "eventType": message.event_type,
        "version": message.version,
        "occurredAt": message.occurred_at,
        "correlationId": message.correlation_id,
        "causationId": message.causation_id if message.HasField("causation_id") else None,
        "producer": message.producer,
        "payload": {
            "trainingSessionId": message.payload.training_session_id,
            "trainingId": message.payload.training_id,
            "startsAt": message.payload.starts_at,
            "endsAt": message.payload.ends_at,
            "capacity": message.payload.capacity,
            "referencePrice": {
                "amountMinor": message.payload.reference_price.amount_minor,
                "currency": message.payload.reference_price.currency,
            },
            "status": message.payload.status,
        },
    }


def encode_protobuf(event: dict[str, Any]) -> bytes:
    return cast(bytes, to_proto(event).SerializeToString(deterministic=True))


def decode_protobuf(data: bytes) -> dict[str, Any]:
    message = TrainingSessionCreatedV1()
    message.ParseFromString(data)
    return from_proto(message)


def avro_schema() -> dict[str, Any]:
    path = ROOT / "contracts/avro/training-session-created.v1.avsc"
    return cast(dict[str, Any], parse_schema(json.loads(path.read_text(encoding="utf-8"))))


def encode_avro(event: dict[str, Any]) -> bytes:
    output = io.BytesIO()
    schemaless_writer(output, avro_schema(), event)
    return output.getvalue()


def decode_avro(data: bytes) -> dict[str, Any]:
    value = schemaless_reader(io.BytesIO(data), avro_schema())  # type: ignore[call-arg]
    return cast(dict[str, Any], value)
