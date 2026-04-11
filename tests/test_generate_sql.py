from app.nodes.generate_sql import generate_sql_node
from tests.mocks import FakeSQLLLM


def test_generate_sql_node_creates_sql(monkeypatch, base_state):
    monkeypatch.setattr(
        "app.nodes.generate_sql.get_llm",
        lambda **kwargs: FakeSQLLLM(),
    )

    result = generate_sql_node(base_state)

    assert not result["error"]
    sql = result["generated_sql"].strip().lower()
    assert sql.startswith("select")
    assert "from students" in sql
    assert "count(" in sql
    assert any(step["step"] == "generate_sql" for step in result["trace"])


def test_generate_sql_handles_llm_exception(monkeypatch, base_state):
    class FailingLLM:
        def invoke(self, prompt: str):
            raise RuntimeError("LLM is down")

    monkeypatch.setattr(
        "app.nodes.generate_sql.get_llm",
        lambda **kwargs: FailingLLM(),
    )

    result = generate_sql_node(base_state)

    assert "SQL generation failed" in result["error"]
    assert result["last_error_stage"] == "generate_sql"
    assert result["trace"][-1]["step"] == "generate_sql_error"