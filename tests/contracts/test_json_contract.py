import json
from pathlib import Path

from astrobridge.contracts.validation import validate_event

ROOT = Path(__file__).resolve().parents[2]


def test_all_valid_fixtures_conform() -> None:
    paths = list((ROOT / "fixtures/valid").glob("training-session-created.v1.json"))
    assert paths
    assert all(not validate_event(json.loads(path.read_text(encoding="utf-8"))) for path in paths)


def test_all_targeted_invalid_fixtures_fail() -> None:
    paths = list((ROOT / "fixtures/invalid").glob("*.json"))
    assert paths
    assert all(validate_event(json.loads(path.read_text(encoding="utf-8"))) for path in paths)


def test_json_round_trip_is_lossless() -> None:
    path = ROOT / "contracts/examples/training-session-created.v1.valid.json"
    event = json.loads(path.read_text(encoding="utf-8"))
    assert json.loads(json.dumps(event, sort_keys=True)) == event
