import json
from pathlib import Path
from typing import Any

import pytest

from astrobridge.contracts.validation import assert_valid_event, validate_event

ROOT = Path(__file__).resolve().parents[2]


def load(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def test_valid_event_has_no_error() -> None:
    assert validate_event(load("fixtures/valid/training-session-created.v1.json")) == []


def test_capacity_error_has_precise_path_and_rule() -> None:
    errors = validate_event(load("fixtures/invalid/capacity-zero.json"))
    assert any(error.path == "$.payload.capacity" and error.rule == "minimum" for error in errors)


def test_cross_field_error_is_readable() -> None:
    errors = validate_event(load("fixtures/invalid/end-before-start.json"))
    assert str(errors[-1]) == (
        "$.payload.endsAt: must be strictly after $.payload.startsAt (rule: strictlyAfter)"
    )


@pytest.mark.parametrize("value", [[], None, "texte", 42, True])
def test_non_object_root_is_a_controlled_contract_error(value: Any) -> None:
    errors = validate_event(value)
    assert [(error.path, error.rule, error.message) for error in errors] == [
        ("$", "type", "expected a JSON object")
    ]
    with pytest.raises(ValueError, match=r"^\$: expected a JSON object \(rule: type\)$"):
        assert_valid_event(value)
