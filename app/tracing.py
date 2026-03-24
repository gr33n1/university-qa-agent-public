from __future__ import annotations
from typing import Any


def append_trace(state: dict[str, Any], step: str, payload: dict[str, Any]) -> None:
    if "trace" not in state:
        state["trace"] = []
    state["trace"].append(
        {
            "step": step,
            "payload": payload,
        }
    )