from __future__ import annotations

import json
import time
from pathlib import Path

import pika
import pytest

from astrobridge.config import Settings
from astrobridge.messaging.consumer import consume_once
from astrobridge.messaging.publisher import publish_event
from astrobridge.messaging.topology import (
    CONSUMERS,
    EVENT_EXCHANGE,
    ROUTING_KEY,
    connection_parameters,
    declare_topology,
)

pytestmark = pytest.mark.integration
ROOT = Path(__file__).resolve().parents[2]
EVENT = json.loads((ROOT / "fixtures/valid/training-session-created.v1.json").read_text())


def parameters(settings: Settings) -> pika.ConnectionParameters:
    return connection_parameters(
        settings.rabbitmq_host,
        settings.rabbitmq_port,
        settings.rabbitmq_user,
        settings.rabbitmq_password,
    )


def clean_queues(settings: Settings) -> None:
    with pika.BlockingConnection(parameters(settings)) as connection:
        channel = connection.channel()
        declare_topology(channel)
        for queue in CONSUMERS.values():
            channel.queue_purge(queue=queue)
            channel.queue_purge(queue=f"{queue}.retry")
            channel.queue_purge(queue=f"{queue}.dlq")


def test_confirmed_publication_two_consumers_and_duplicate(tmp_path: Path) -> None:
    settings = Settings(data_dir=tmp_path)
    clean_queues(settings)
    assert publish_event(EVENT, settings)
    assert consume_once("administration", settings) == "processed"
    assert consume_once("notification", settings) == "processed"
    assert publish_event(EVENT, settings)
    assert consume_once("administration", settings) == "duplicate"
    assert consume_once("notification", settings) == "duplicate"
    for consumer in CONSUMERS:
        traces = (tmp_path / f"evidence-{consumer}.jsonl").read_text().splitlines()
        effects = [line for line in traces if "prepared" in line or "traced" in line]
        assert len(effects) == 1


def test_poison_message_reaches_dlq_after_bounded_retries(tmp_path: Path) -> None:
    settings = Settings(data_dir=tmp_path)
    clean_queues(settings)
    with pika.BlockingConnection(parameters(settings)) as connection:
        channel = connection.channel()
        declare_topology(channel)
        channel.basic_publish(
            exchange=EVENT_EXCHANGE,
            routing_key=ROUTING_KEY,
            body=b"not-json",
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent,
                correlation_id="synthetic-poison",
                headers={"x-retry-count": 0},
            ),
        )
    for _ in range(4):
        result = consume_once("administration", settings)
        assert result in {"retry", "dead-letter"}
        time.sleep(0.7)
    with pika.BlockingConnection(parameters(settings)) as connection:
        channel = connection.channel()
        method, properties, body = channel.basic_get(
            queue=f"{CONSUMERS['administration']}.dlq", auto_ack=True
        )
        assert method is not None
        assert body == b"not-json"
        assert properties.headers["x-retry-count"] == 4


def test_valid_json_array_reaches_dlq_after_bounded_retries(tmp_path: Path) -> None:
    settings = Settings(data_dir=tmp_path)
    clean_queues(settings)
    with pika.BlockingConnection(parameters(settings)) as connection:
        channel = connection.channel()
        declare_topology(channel)
        channel.basic_publish(
            exchange=EVENT_EXCHANGE,
            routing_key=ROUTING_KEY,
            body=b"[]",
            properties=pika.BasicProperties(
                content_type="application/json",
                delivery_mode=pika.DeliveryMode.Persistent,
                message_id="synthetic-non-object",
                correlation_id="synthetic-non-object",
                headers={"x-retry-count": 0, "x-original": "kept"},
            ),
        )
    for _ in range(4):
        result = consume_once("administration", settings)
        assert result in {"retry", "dead-letter"}
        time.sleep(0.7)
    with pika.BlockingConnection(parameters(settings)) as connection:
        channel = connection.channel()
        method, properties, body = channel.basic_get(
            queue=f"{CONSUMERS['administration']}.dlq", auto_ack=True
        )
        assert method is not None
        assert body == b"[]"
        assert properties.message_id == "synthetic-non-object"
        assert properties.correlation_id == "synthetic-non-object"
        assert properties.headers["x-original"] == "kept"
        assert properties.headers["x-retry-count"] == 4


def test_unacked_message_is_redelivered_after_consumer_restart(tmp_path: Path) -> None:
    settings = Settings(data_dir=tmp_path)
    clean_queues(settings)
    assert publish_event(EVENT, settings)
    connection = pika.BlockingConnection(parameters(settings))
    channel = connection.channel()
    method, _, _ = channel.basic_get(queue=CONSUMERS["administration"], auto_ack=False)
    assert method is not None
    connection.close()
    with pika.BlockingConnection(parameters(settings)) as restarted:
        channel = restarted.channel()
        method, _, _ = channel.basic_get(queue=CONSUMERS["administration"], auto_ack=False)
        assert method is not None and method.redelivered
        channel.basic_ack(method.delivery_tag)
