from __future__ import annotations

import json
from typing import Any

import pika  # type: ignore[import-untyped]

from astrobridge.config import Settings
from astrobridge.contracts.validation import assert_valid_event
from astrobridge.messaging.topology import (
    EVENT_EXCHANGE,
    ROUTING_KEY,
    connection_parameters,
    declare_topology,
)


def publish_event(event: dict[str, Any], settings: Settings | None = None) -> bool:
    assert_valid_event(event)
    active = settings or Settings()
    parameters = connection_parameters(
        active.rabbitmq_host,
        active.rabbitmq_port,
        active.rabbitmq_user,
        active.rabbitmq_password,
    )
    with pika.BlockingConnection(parameters) as connection:
        channel = connection.channel()
        declare_topology(channel)
        channel.confirm_delivery()
        channel.basic_publish(
            exchange=EVENT_EXCHANGE,
            routing_key=ROUTING_KEY,
            body=json.dumps(event, separators=(",", ":")).encode(),
            properties=pika.BasicProperties(
                content_type="application/json",
                delivery_mode=pika.DeliveryMode.Persistent,
                message_id=event["eventId"],
                correlation_id=event["correlationId"],
                headers={"x-retry-count": 0},
            ),
            mandatory=True,
        )
        return True
