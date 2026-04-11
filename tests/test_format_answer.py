from app.nodes.format_answer import format_answer_node


def test_format_answer_handles_llm_exception(monkeypatch):
    class FailingLLM:
        def invoke(self, prompt: str):
            raise RuntimeError("LLM formatting failed")

    monkeypatch.setattr(
        "app.nodes.format_answer.get_llm",
        lambda **kwargs: FailingLLM(),
    )

    state = {
        "question": "How many students are there?",
        "query_result": [{"student_count": 6}],
        "trace": [],
    }

    result = format_answer_node(state)

    assert "Answer formatting failed" in result["error"]
    assert result["last_error_stage"] == "format_answer"
    assert result["final_answer"] == (
        "I found the database result, but failed to format the final answer."
    )
    assert result["trace"][-1]["step"] == "format_answer_error"