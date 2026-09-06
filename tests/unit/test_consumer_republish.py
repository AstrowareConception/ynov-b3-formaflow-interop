from unittest.mock import Mock

import pika
import pytest

from astrobridge.messaging.consumer import RepublishError, _republish_failed_message


def properties() -> pika.BasicProperties:
    return pika.BasicProperties(
        content_type="application/json",
        content_encoding="utf-8",
        headers={"x-original": "kept"},
        delivery_mode=pika.DeliveryMode.Persistent,
        priority=2,
        correlation_id="synthetic-correlation",
        reply_to="synthetic.reply",
        expiration="1000",
        message_id="synthetic-message",
        timestamp=1_789_000_000,
        type="TrainingSessionCreated",
        app_id="astrobridge-test",
    )


def test_confirmed_retry_is_published_before_original_ack() -> None:
    channel = Mock()
    _republish_failed_message(
        channel,
        delivery_tag=17,
        properties=properties(),
        body=b"{}",
        exchange="astrobridge.retry",
        routing_key="administration",
        headers={"x-original": "kept", "x-retry-count": 1},
    )

    channel.confirm_delivery.assert_called_once_with()
    published = channel.basic_publish.call_args.kwargs
    assert published["mandatory"] is True
    assert published["properties"].message_id == "synthetic-message"
    assert published["properties"].correlation_id == "synthetic-correlation"
    assert published["properties"].headers["x-original"] == "kept"
    assert published["properties"].headers["x-retry-count"] == 1
    channel.basic_ack.assert_called_once_with(delivery_tag=17)
    channel.basic_nack.assert_not_called()


def test_negative_publish_confirmation_nacks_without_ack() -> None:
    channel = Mock()
    channel.basic_publish.side_effect = pika.exceptions.NackError([])

    with pytest.raises(RepublishError, match="was not confirmed"):
        _republish_failed_message(
            channel,
            delivery_tag=23,
            properties=properties(),
            body=b"[]",
            exchange="astrobridge.retry",
            routing_key="administration",
            headers={"x-retry-count": 1},
        )

    channel.basic_nack.assert_called_once_with(delivery_tag=23, requeue=True)
    channel.basic_ack.assert_not_called()
