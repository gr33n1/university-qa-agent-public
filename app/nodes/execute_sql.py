from app.db.repository import DatabaseRepository
from app.tracing import append_trace


def execute_sql_node(state: dict) -> dict:
    if state.get("error"):
        append_trace(
            state,
            "execute_sql_skipped",
            {
                "reason": "previous_error",
                "error": state["error"],
            },
        )
        return state

    sql = state.get("validated_sql", "")
    repo = DatabaseRepository()

    try:
        result = repo.execute_select(sql)
        state["query_result"] = result

        append_trace(
            state,
            "execute_sql",
            {
                "sql": sql,
                "row_count": len(result),
                "query_result": result,
            },
        )
    except Exception as exc:
        state["error"] = str(exc)
        state["query_result"] = []

        append_trace(
            state,
            "execute_sql_error",
            {
                "sql": sql,
                "error": str(exc),
            },
        )

    return state