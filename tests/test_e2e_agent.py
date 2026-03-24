from app.graph import build_graph


class FakeResponse:
    def __init__(self, content: str):
        self.content = content


class FakeSQLLLM:
    def __init__(self, *args, **kwargs):
        pass

    def invoke(self, prompt: str):
        return FakeResponse(
            """
            SELECT COUNT(*) AS student_count
            FROM students;
            """
        )


class FakeAnswerLLM:
    def __init__(self, *args, **kwargs):
        pass

    def invoke(self, prompt: str):
        return FakeResponse("There are 6 students in the database.")


def test_e2e_agent_with_natural_language(monkeypatch):
    monkeypatch.setattr(
        "app.nodes.generate_sql.ChatGoogleGenerativeAI",
        FakeSQLLLM,
    )
    monkeypatch.setattr(
        "app.nodes.format_answer.ChatGoogleGenerativeAI",
        FakeAnswerLLM,
    )

    graph = build_graph()

    initial_state = {
        "question": "How many students are there?",
        "trace": [],
    }

    result = graph.invoke(initial_state)

    assert result.get("error") is None
    assert result["generated_sql"].strip().lower().startswith("select")
    assert result["validated_sql"].strip().lower().startswith("select")
    assert result["final_answer"] == "There are 6 students in the database."

    trace_steps = [item["step"] for item in result["trace"]]
    assert trace_steps == [
        "guard_input_passed",
        "load_schema",
        "generate_sql",
        "validate_sql",
        "execute_sql",
        "format_answer",
    ]


def test_e2e_agent_blocks_destructive_input():
    graph = build_graph()

    initial_state = {
        "question": "DELETE FROM students",
        "trace": [],
    }

    result = graph.invoke(initial_state)

    assert result.get("error") is not None
    assert "not allowed" in result["final_answer"].lower()

    trace_steps = [item["step"] for item in result["trace"]]
    assert "guard_input_blocked" in trace_steps
    assert "format_answer_error" in trace_steps
    assert "execute_sql" not in trace_steps