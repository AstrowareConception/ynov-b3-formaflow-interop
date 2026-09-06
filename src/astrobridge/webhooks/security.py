from __future__ import annotations

import hashlib
import hmac
import time


def signature(secret: str, timestamp: int, idempotency_key: str, body: bytes) -> str:
    signed = str(timestamp).encode() + b"." + idempotency_key.encode() + b"." + body
    return hmac.new(secret.encode(), signed, hashlib.sha256).hexdigest()


class ReplayGuard:
    def __init__(self, max_age_seconds: int = 300) -> None:
        self.max_age_seconds = max_age_seconds
        self.seen: set[str] = set()

    def verify(
        self,
        secret: str,
        timestamp: int,
        idempotency_key: str,
        body: bytes,
        supplied_signature: str,
        *,
        now: int | None = None,
    ) -> bool:
        current = int(time.time()) if now is None else now
        if abs(current - timestamp) > self.max_age_seconds or idempotency_key in self.seen:
            return False
        expected = signature(secret, timestamp, idempotency_key, body)
        if not hmac.compare_digest(expected, supplied_signature):
            return False
        self.seen.add(idempotency_key)
        return True

