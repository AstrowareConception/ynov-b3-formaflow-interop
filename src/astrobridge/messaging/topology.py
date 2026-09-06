from __future__ import annotations

from typing import Any

import pika  # type: ignore[import-untyped]

EVENT_EXCHANGE = "formaflow.events"
ROUTING_KEY = "training.session.created.v1"
RETRY_EXCHANGE = "astrobridge.retry"
DEAD_LETTER_EXCHANGE = "astrobridge.dead-letter"
CONSUMERS = {
    "administration": "astrobridge.administration.training-session-created.v1",
    "notification": "astrobridge.notification.training-session-created.v1",
}
MAX_RETRIES = 3


def declare_topology(channel: Any) -> None:
    channel.exchange_declare(exchange=EVENT_EXCHANGE, exchange_type="topic", durable=True)
    channel.exchange_declare(exchange=RETRY_EXCHANGE, exchange_type="direct", durable=True)
    channel.exchange_declare(
        exchange=DEAD_LETTER_EXCHANGE, exchange_type="direct", durable=True
    )
    for consumer, queue in CONSUMERS.items():
        retry_queue = f"{queue}.retry"
        dead_queue = f"{queue}.dlq"
        channel.queue_declare(queue=queue, durable=True)
        channel.queue_bind(queue=queue, exchange=EVENT_EXCHANGE, routing_key=ROUTING_KEY)
        channel.queue_declare(
            queue=retry_queue,
            durable=True,
            arguments={
                "x-message-ttl": 500,
                "x-dead-letter-exchange": "",
                "x-dead-letter-routing-key": queue,
            },
        )
        channel.queue_bind(queue=retry_queue, exchange=RETRY_EXCHANGE, routing_key=consumer)
        channel.queue_declare(queue=dead_queue, durable=True)
        channel.queue_bind(
            queue=dead_queue, exchange=DEAD_LETTER_EXCHANGE, routing_key=consumer
        )


def connection_parameters(
    host: str, port: int, user: str, password: str
) -> pika.ConnectionParameters:
    return pika.ConnectionParameters(
        host=host,
        port=port,
        credentials=pika.PlainCredentials(user, password),
        heartbeat=30,
        blocked_connection_timeout=10,
    )
