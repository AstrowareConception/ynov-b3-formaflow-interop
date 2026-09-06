from __future__ import annotations

import json
from typing import Any, NoReturn, cast

import pika  # type: ignore[import-untyped]

from astrobridge.config import Settings
from astrobridge.contracts.validation import assert_valid_event
from astrobridge.messaging.topology import (
    CONSUMERS,
    DEAD_LETTER_EXCHANGE,
    MAX_RETRIES,
    RETRY_EXCHANGE,
    connection_parameters,
    declare_topology,
)
from astrobridge.observability.store import EvidenceStore


class ConsumerProcessor:
    def __init__(self, consumer: str, store: EvidenceStore) -> None:
        if consumer not in CONSUMERS:
            raise ValueError(f"unknown consumer: {consumer}")
        self.consumer = consumer
        self.store = store

    def process(self, event: Any, retry_count: int = 0, failure_until: int = 0) -> str:
        assert_valid_event(event)
        event_dict = cast(dict[str, Any], event)
        event_id = str(event_dict["eventId"])
        if self.store.contains(self.consumer, event_id):
            self.store.record(self.consumer, event_dict, "duplicate-ignored")
            return "duplicate"
        if retry_count < failure_until:
            raise RuntimeError("synthetic injected consumer failure")
        outcome = (
            "administration-prepared"
            if self.consumer == "administration"
            else "notification-traced"
        )
        self.store.record(self.consumer, event_dict, outcome)
        self.store.mark(self.consumer, event_id)
        return "processed"


class RepublishError(RuntimeError):
    """Retry or DLQ publication was not confirmed by RabbitMQ."""


def _reject_unconfirmed(channel: Any, delivery_tag: int, error: Exception) -> NoReturn:
    channel.basic_nack(delivery_tag=delivery_tag, requeue=True)
    raise RepublishError("retry or DLQ publication was not confirmed") from error


def _republish_failed_message(
    channel: Any,
    *,
    delivery_tag: int,
    properties: Any,
    body: bytes,
    exchange: str,
    routing_key: str,
    headers: dict[str, Any],
) -> None:
    republished_properties = pika.BasicProperties(
        content_type=properties.content_type or "application/json",
        content_encoding=properties.content_encoding,
        headers=headers,
        delivery_mode=properties.delivery_mode or pika.DeliveryMode.Persistent,
        priority=properties.priority,
        correlation_id=properties.correlation_id,
        reply_to=properties.reply_to,
        expiration=properties.expiration,
        message_id=properties.message_id,
        timestamp=properties.timestamp,
        type=properties.type,
        user_id=properties.user_id,
        app_id=properties.app_id,
        cluster_id=properties.cluster_id,
    )
    try:
        channel.confirm_delivery()
        channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=body,
            properties=republished_properties,
            mandatory=True,
        )
    except (pika.exceptions.NackError, pika.exceptions.UnroutableError) as error:
        _reject_unconfirmed(channel, delivery_tag, error)
    except pika.exceptions.AMQPError as error:
        _reject_unconfirmed(channel, delivery_tag, error)
    channel.basic_ack(delivery_tag=delivery_tag)


def consume_once(consumer: str, settings: Settings | None = None) -> str:
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
        channel.basic_qos(prefetch_count=1)
        method, properties, body = channel.basic_get(queue=CONSUMERS[consumer], auto_ack=False)
        if method is None:
            return "empty"
        retry_count = int((properties.headers or {}).get("x-retry-count", 0))
        processor = ConsumerProcessor(consumer, EvidenceStore(active.data_dir))
        try:
            event = json.loads(body)
            failure_until = int((properties.headers or {}).get("x-fail-until", 0))
            result = processor.process(event, retry_count, failure_until)
        except (ValueError, RuntimeError, json.JSONDecodeError) as error:
            headers = dict(properties.headers or {})
            headers["x-retry-count"] = retry_count + 1
            headers["x-last-error"] = type(error).__name__
            if retry_count < MAX_RETRIES:
                exchange = RETRY_EXCHANGE
                routing_key = consumer
                result = "retry"
            else:
                exchange = DEAD_LETTER_EXCHANGE
                routing_key = consumer
                result = "dead-letter"
            _republish_failed_message(
                channel,
                delivery_tag=method.delivery_tag,
                properties=properties,
                body=body,
                exchange=exchange,
                routing_key=routing_key,
                headers=headers,
            )
            return result
        channel.basic_ack(delivery_tag=method.delivery_tag)
        return result
