from app.nodes.validate_sql import validate_sql_node


def test_validate_sql_accepts_select():
    state = {"generated_sql": "SELECT * FROM students"}
    result = validate_sql_node(state)
    assert result.get("error") is None
    assert result["validated_sql"] == "SELECT * FROM students"


def test_validate_sql_rejects_delete():
    state = {"generated_sql": "DELETE FROM students"}
    result = validate_sql_node(state)
    assert result.get("error") is not None


def test_validate_sql_rejects_empty():
    state = {"generated_sql": "   "}
    result = validate_sql_node(state)
    assert result.get("error") is not None


def test_validate_sql_rejects_non_select_update():
    state = {"generated_sql": "UPDATE students SET major = 'CS'"}
    result = validate_sql_node(state)
    assert result.get("error") is not None
    assert "only select" in result["error"].lower()


def test_validate_sql_rejects_multiple_statements():
    state = {"generated_sql": "SELECT * FROM students; DELETE FROM students;"}
    result = validate_sql_node(state)
    assert result.get("error") is not None