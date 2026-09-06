from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, cast

from jsonschema import Draft202012Validator, FormatChecker  # type: ignore[import-untyped]

ROOT = Path(__file__).resolve().parents[3]


@dataclass(frozen=True)
class ContractError:
    path: str
    rule: str
    message: str

    def __str__(self) -> str:
        return f"{self.path}: {self.message} (rule: {self.rule})"


def _path(parts: list[str | int]) -> str:
    return "$" + "".join(f"[{part}]" if isinstance(part, int) else f".{part}" for part in parts)


def load_schema(version: int = 1) -> dict[str, Any]:
    path = ROOT / f"contracts/json-schema/training-session-created.v{version}.schema.json"
    return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))


def validate_event(event: Any, *, version: int = 1) -> list[ContractError]:
    if not isinstance(event, dict):
        return [ContractError("$", "type", "expected a JSON object")]
    validator = Draft202012Validator(load_schema(version), format_checker=FormatChecker())
    errors = [
        ContractError(_path(list(error.absolute_path)), error.validator, error.message)
        for error in sorted(validator.iter_errors(event), key=lambda item: list(item.absolute_path))
    ]
    payload = event.get("payload")
    has_dates = (
        isinstance(payload, dict)
        and isinstance(payload.get("startsAt"), str)
        and isinstance(payload.get("endsAt"), str)
    )
    if has_dates:
        payload_dict = cast(dict[str, Any], payload)
        try:
            starts = datetime.fromisoformat(payload_dict["startsAt"].replace("Z", "+00:00"))
            ends = datetime.fromisoformat(payload_dict["endsAt"].replace("Z", "+00:00"))
            if ends <= starts:
                errors.append(
                    ContractError(
                        "$.payload.endsAt",
                        "strictlyAfter",
                        "must be strictly after $.payload.startsAt",
                    )
                )
        except ValueError:
            pass
    return errors


def assert_valid_event(event: Any, *, version: int = 1) -> None:
    errors = validate_event(event, version=version)
    if errors:
        raise ValueError("\n".join(str(error) for error in errors))
