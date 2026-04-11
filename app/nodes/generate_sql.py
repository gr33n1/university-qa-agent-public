from app.llm import get_llm
from app.prompts import SQL_GENERATION_PROMPT
from app.tracing import append_trace


def generate_sql_node(state: dict) -> dict:
    question = state["question"]
    schema_context = state["schema_context"]

    llm = get_llm()

    prompt = SQL_GENERATION_PROMPT.format(
        question=question,
        schema_context=schema_context,
    )

    try:
        response = llm.invoke(prompt)
    except Exception as e:
        state["error"] = f"SQL generation failed: {e}"
        state["last_error_stage"] = "generate_sql"

        append_trace(
            state,
            "generate_sql_error",
            {
                "question": question,
                "error": str(e),
            },
        )
        return state

    sql = response.content.strip()
    state["generated_sql"] = sql

    append_trace(
        state,
        "generate_sql",
        {
            "question": question,
            "generated_sql": sql,
            "provider": "gemini",
            "model": "gemini-2.5-flash",
        },
    )
    return state