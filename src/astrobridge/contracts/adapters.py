from __future__ import annotations

from copy import deepcopy
from typing import Any


def upcast_v1_to_v2(event: dict[str, Any]) -> dict[str, Any]:
    if event.get("version") != 1:
        raise ValueError("upcast expects a V1 event")
    adapted = deepcopy(event)
    adapted["version"] = 2
    adapted["payload"]["deliveryMode"] = "ONSITE"
    adapted["payload"]["location"] = {"label": "TO_BE_CONFIRMED"}
    return adapted


def downcast_v2_to_v1(event: dict[str, Any]) -> dict[str, Any]:
    if event.get("version") != 2:
        raise ValueError("downcast expects a V2 event")
    adapted = deepcopy(event)
    adapted["version"] = 1
    adapted["payload"].pop("deliveryMode", None)
    adapted["payload"].pop("location", None)
    return adapted
