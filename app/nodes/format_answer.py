from app.llm import get_llm
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

    llm = get_llm()

    prompt = ANSWER_FORMATTING_PROMPT.format(
        question=question,
        query_result=query_result,
    )

    try:
        response = llm.invoke(prompt)
    except Exception as e:
        state["error"] = f"Answer formatting failed: {e}"
        state["last_error_stage"] = "format_answer"
        state["final_answer"] = "I found the database result, but failed to format the final answer."

        append_trace(
            state,
            "format_answer_error",
            {
                "error": str(e),
                "final_answer": state["final_answer"],
            },
        )
        return state

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