import pytest


@pytest.fixture
def base_state():
    return {
        "question": "How many students are there?",
        "normalized_question": "How many students are there?",
        "schema_context": "CREATE TABLE students (id INTEGER, name TEXT);",
        "sql_query": "",
        "query_result": None,
        "final_answer": "",
        "error": "",
        "trace": [],
        "request_id": "test-request-id",
        "repair_attempts": 0,
        "last_failed_stage": "",
    }