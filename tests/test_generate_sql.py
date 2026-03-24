from app.nodes.generate_sql import generate_sql_node


class FakeResponse:
    def __init__(self, content: str):
        self.content = content


class FakeLLM:
    def __init__(self, *args, **kwargs):
        pass

    def invoke(self, prompt: str):
        return FakeResponse(
            """
            SELECT COUNT(*) AS student_count
            FROM students;
            """
        )


def test_generate_sql_node_creates_sql(monkeypatch):
    monkeypatch.setattr(
        "app.nodes.generate_sql.ChatGoogleGenerativeAI",
        FakeLLM,
    )

    state = {
        "question": "How many students are there?",
        "schema_context": "dummy schema",
        "trace": [],
    }

    result = generate_sql_node(state)

    assert result.get("error") is None
    assert result["generated_sql"].strip() == "SELECT COUNT(*) AS student_count\n            FROM students;"
    assert any(step["step"] == "generate_sql" for step in result["trace"])