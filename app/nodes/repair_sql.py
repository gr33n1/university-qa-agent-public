from langchain_google_genai import ChatGoogleGenerativeAI

from app.llm import get_llm
from app.prompts import SQL_REPAIR_PROMPT
from app.tracing import append_trace


def repair_sql_node(state: dict) -> dict:
    if state.get("repair_attempts", 0) >= state.get("max_repair_attempts", 1):
        append_trace(
            state,
            "repair_sql_skipped",
            {
                "reason": "max_attempts_reached",
                "repair_attempts": state.get("repair_attempts", 0),
            },
        )
        return state

    question = state["question"]
    schema_context = state["schema_context"]
    failed_sql = state.get("failed_sql", "")
    error_message = state.get("error", "") or state.get("last_db_error", "")

    llm = get_llm()

    prompt = SQL_REPAIR_PROMPT.format(
        question=question,
        schema_context=schema_context,
        failed_sql=failed_sql,
        error_message=error_message,
    )

    try:
        response = llm.invoke(prompt)
        repaired_sql = response.content.strip()

        state["generated_sql"] = repaired_sql
        state["validated_sql"] = ""
        state["error"] = ""
        state["repair_attempts"] = state.get("repair_attempts", 0) + 1

        append_trace(
            state,
            "repair_sql",
            {
                "failed_sql": failed_sql,
                "error_message": error_message,
                "repaired_sql": repaired_sql,
                "repair_attempts": state["repair_attempts"],
            },
        )
    except Exception as exc:
        state["error"] = f"Failed to repair SQL: {exc}"
        state["last_error_stage"] = "repair_sql"

        append_trace(
            state,
            "repair_sql_error",
            {
                "failed_sql": failed_sql,
                "error_message": error_message,
                "repair_error": state["error"],
                "repair_attempts": state["repair_attempts"],
            },
        )

    return state