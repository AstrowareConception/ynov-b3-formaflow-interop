from astrobridge.webhooks.security import ReplayGuard, signature


def test_hmac_signature_and_replay_protection() -> None:
    body = b'{"synthetic":true}'
    secret = "synthetic_demo_secret_change_me"  # noqa: S105 - explicit fake fixture
    supplied = signature(secret, 1000, "event-1", body)
    guard = ReplayGuard(max_age_seconds=300)
    assert guard.verify(secret, 1000, "event-1", body, supplied, now=1100)
    assert not guard.verify(secret, 1000, "event-1", body, supplied, now=1100)


def test_old_or_tampered_webhook_is_rejected() -> None:
    guard = ReplayGuard(max_age_seconds=300)
    assert not guard.verify("secret", 1000, "event-2", b"body", "bad", now=1000)
    valid = signature("secret", 1000, "event-3", b"body")
    assert not guard.verify("secret", 1000, "event-3", b"body", valid, now=1400)
