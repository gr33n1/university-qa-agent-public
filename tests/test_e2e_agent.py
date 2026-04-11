from app.graph import build_graph
from tests.mocks import FakeSQLLLM, FakeAnswerLLM


def test_e2e_agent_with_natural_language(monkeypatch):
    monkeypatch.setattr(
        "app.nodes.generate_sql.get_llm",
        lambda **kwargs: FakeSQLLLM(),
    )
    monkeypatch.setattr(
        "app.nodes.format_answer.get_llm",
        lambda **kwargs: FakeAnswerLLM(),
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
    assert "6" in result["final_answer"]
    assert "students" in result["final_answer"].lower()

    trace_steps = [item["step"] for item in result["trace"]]
    assert "guard_input_passed" in trace_steps
    assert "load_schema" in trace_steps
    assert "generate_sql" in trace_steps
    assert "validate_sql" in trace_steps
    assert "execute_sql" in trace_steps
    assert "format_answer" in trace_steps
    assert trace_steps.index("generate_sql") < trace_steps.index("validate_sql")
    assert trace_steps.index("validate_sql") < trace_steps.index("execute_sql")
    assert trace_steps.index("execute_sql") < trace_steps.index("format_answer")


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