from app.tracing import append_trace


def test_append_trace_adds_required_fields():
    state = {"trace": []}

    append_trace(state, "test_step", {"x": 1})

    event = state["trace"][0]

    assert event["step"] == "test_step"
    assert event["payload"] == {"x": 1}
    assert "request_id" in event
    assert "event_index" in event
    assert "timestamp_utc" in event