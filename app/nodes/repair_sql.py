from langchain_google_genai import ChatGoogleGenerativeAI

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
    error_message = state.get("last_db_error") or state.get("error", "")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
    )

    prompt = SQL_REPAIR_PROMPT.format(
        question=question,
        schema_context=schema_context,
        failed_sql=failed_sql,
        error_message=error_message,
    )

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

    return state