import json
from pathlib import Path

import pytest

from astrobridge.messaging.consumer import ConsumerProcessor
from astrobridge.observability.store import EvidenceStore

ROOT = Path(__file__).resolve().parents[2]
EVENT = json.loads((ROOT / "fixtures/valid/training-session-created.v1.json").read_text())


def test_duplicate_has_no_second_effect(tmp_path: Path) -> None:
    processor = ConsumerProcessor("administration", EvidenceStore(tmp_path))
    assert processor.process(EVENT) == "processed"
    assert processor.process(EVENT) == "duplicate"
    lines = (tmp_path / "evidence-administration.jsonl").read_text().splitlines()
    assert len(lines) == 2
    assert "duplicate-ignored" in lines[-1]


def test_failure_injection_is_bounded_by_retry_count(tmp_path: Path) -> None:
    processor = ConsumerProcessor("notification", EvidenceStore(tmp_path))
    with pytest.raises(RuntimeError, match="synthetic injected"):
        processor.process(EVENT, retry_count=1, failure_until=2)
    assert processor.process(EVENT, retry_count=2, failure_until=2) == "processed"
