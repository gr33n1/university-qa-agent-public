from __future__ import annotations

from datetime import datetime, UTC
from typing import Any
from uuid import uuid4


def append_trace(state: dict[str, Any], step: str, payload: dict[str, Any]) -> None:
    if "trace" not in state:
        state["trace"] = []

    if not state.get("request_id"):
        state["request_id"] = str(uuid4())

    state["trace"].append(
        {
            "request_id": state["request_id"],
            "event_index": len(state["trace"]) + 1,
            "timestamp_utc": datetime.now(UTC).isoformat(),
            "step": step,
            "payload": payload,
        }
    )