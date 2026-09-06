import json
from pathlib import Path

from astrobridge.contracts.adapters import downcast_v2_to_v1, upcast_v1_to_v2
from astrobridge.contracts.validation import validate_event

ROOT = Path(__file__).resolve().parents[2]


def load(name: str) -> dict:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def test_v2_downcast_keeps_old_client_contract() -> None:
    event_v2 = load("contracts/examples/training-session-created.v2.valid.json")
    legacy = downcast_v2_to_v1(event_v2)
    assert legacy["version"] == 1
    assert "deliveryMode" not in legacy["payload"]
    assert validate_event(legacy, version=1) == []


def test_v1_upcast_uses_explicit_defaults() -> None:
    event_v1 = load("contracts/examples/training-session-created.v1.valid.json")
    current = upcast_v1_to_v2(event_v1)
    assert current["payload"]["deliveryMode"] == "ONSITE"
    assert current["payload"]["location"] == {"label": "TO_BE_CONFIRMED"}
    assert validate_event(current, version=2) == []
