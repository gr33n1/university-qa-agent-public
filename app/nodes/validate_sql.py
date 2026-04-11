from app.tracing import append_trace
from app.validation.rules import (
    FORBIDDEN_SQL_KEYWORDS,
    MAX_SQL_LENGTH,
)


def validate_sql_node(state: dict) -> dict:
    sql = state.get("generated_sql", "")

    if state.get("error"):
        append_trace(
            state,
            "validate_sql_skipped",
            {
                "reason": "previous_error",
                "error": state["error"],
            },
        )
        return state

    if not sql or not sql.strip():
        state["error"] = "Generated SQL is empty."
        state["last_error_stage"] = "validate_sql"
        state["failed_sql"] = sql
        append_trace(
            state,
            "validate_sql_error",
            {
                "sql": sql,
                "error": state["error"],
            },
        )
        return state

    sql_clean = sql.strip()
    sql_lower = sql_clean.lower()

    if len(sql_clean) > MAX_SQL_LENGTH:
        state["error"] = "Generated SQL is too long."
        state["last_error_stage"] = "validate_sql"
        state["failed_sql"] = sql_clean
        append_trace(
            state,
            "validate_sql_error",
            {
                "sql": sql_clean,
                "error": state["error"],
            },
        )
        return state

    if not sql_lower.startswith("select"):
        state["error"] = "Only SELECT queries are allowed."
        state["last_error_stage"] = "validate_sql"
        state["failed_sql"] = sql_clean
        append_trace(
            state,
            "validate_sql_error",
            {
                "sql": sql_clean,
                "error": state["error"],
            },
        )
        return state

    if sql_clean.count(";") > 1:
        state["error"] = "Only a single SQL statement is allowed."
        state["last_error_stage"] = "validate_sql"
        state["failed_sql"] = sql_clean
        append_trace(
            state,
            "validate_sql_error",
            {
                "sql": sql_clean,
                "error": state["error"],
            },
        )
        return state

    for keyword in FORBIDDEN_SQL_KEYWORDS:
        if keyword in sql_lower:
            state["error"] = f"Forbidden SQL keyword detected: {keyword}"
            state["last_error_stage"] = "validate_sql"
            state["failed_sql"] = sql_clean
            append_trace(
                state,
                "validate_sql_error",
                {
                    "sql": sql_clean,
                    "error": state["error"],
                },
            )
            return state

    state["validated_sql"] = sql_clean

    append_trace(
        state,
        "validate_sql",
        {
            "status": "passed",
        },
    )
    return state