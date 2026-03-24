from langchain_google_genai import ChatGoogleGenerativeAI

from app.prompts import SQL_GENERATION_PROMPT
from app.tracing import append_trace


def generate_sql_node(state: dict) -> dict:
    question = state["question"]
    schema_context = state["schema_context"]

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
    )

    prompt = SQL_GENERATION_PROMPT.format(
        question=question,
        schema_context=schema_context,
    )

    response = llm.invoke(prompt)
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