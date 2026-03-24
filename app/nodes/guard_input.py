from app.tracing import append_trace
from app.validation.rules import (
    FORBIDDEN_INPUT_PREFIXES,
    SUSPICIOUS_INPUT_PATTERNS,
    MAX_INPUT_LENGTH,
)


def guard_input_node(state: dict) -> dict:
    question = state.get("question", "")

    if question is None:
        state["error"] = "Input question is missing."
        append_trace(state, "guard_input_blocked", {"reason": "missing_input"})
        return state

    if not isinstance(question, str):
        state["error"] = "Input question must be a string."
        append_trace(state, "guard_input_blocked", {"reason": "non_string_input"})
        return state

    raw_question = question
    question = question.strip()
    question_lower = question.lower()

    if not question:
        state["error"] = "Input question is empty."
        append_trace(state, "guard_input_blocked", {"reason": "empty_input"})
        return state

    if len(question) > MAX_INPUT_LENGTH:
        state["error"] = "Input question is too long."
        append_trace(
            state,
            "guard_input_blocked",
            {"reason": "input_too_long", "length": len(question)},
        )
        return state

    if any(ord(ch) < 32 and ch not in ("\n", "\t", "\r") for ch in raw_question):
        state["error"] = "Input contains unsupported control characters."
        append_trace(state, "guard_input_blocked", {"reason": "control_characters"})
        return state

    for prefix in FORBIDDEN_INPUT_PREFIXES:
        if question_lower.startswith(prefix):
            state["error"] = (
                "Direct SQL commands are not allowed. "
                "Please ask a natural-language question about the university database."
            )
            append_trace(
                state,
                "guard_input_blocked",
                {"reason": f"forbidden_prefix:{prefix}", "input": raw_question},
            )
            return state

    suspicious_found = [p for p in SUSPICIOUS_INPUT_PATTERNS if p in question_lower]
    if suspicious_found:
        state["error"] = "Input contains suspicious SQL-like patterns."
        append_trace(
            state,
            "guard_input_blocked",
            {"reason": "suspicious_patterns", "patterns": suspicious_found},
        )
        return state

    if question_lower.count(";") > 0:
        state["error"] = "Please send a single natural-language question without SQL syntax."
        append_trace(
            state,
            "guard_input_blocked",
            {"reason": "semicolon_in_input"},
        )
        return state

    state["question"] = question

    append_trace(
        state,
        "guard_input_passed",
        {"input": raw_question, "normalized_question": question},
    )
    return state