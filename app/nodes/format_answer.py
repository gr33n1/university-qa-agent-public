from langchain_google_genai import ChatGoogleGenerativeAI

from app.prompts import ANSWER_FORMATTING_PROMPT
from app.tracing import append_trace


def format_answer_node(state: dict) -> dict:

    if state.get("error"):
        stage = state.get("last_error_stage", "unknown_stage")
        attempts = state.get("repair_attempts", 0)
        state["final_answer"] = (
            f"I couldn't complete your request after {attempts} repair attempt(s). "
            f"Last failure was in {stage}: {state['error']}"
        )
        append_trace(
            state,
            "format_answer_error",
            {
                "final_answer": state["final_answer"],
            },
        )
        return state

    question = state["question"]
    query_result = state.get("query_result", [])

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
    )

    prompt = ANSWER_FORMATTING_PROMPT.format(
        question=question,
        query_result=query_result,
    )

    response = llm.invoke(prompt)
    final_answer = response.content.strip()

    state["final_answer"] = final_answer

    append_trace(
        state,
        "format_answer",
        {
            "final_answer": final_answer,
            "provider": "gemini",
            "model": "gemini-2.5-flash",
        },
    )
    return state