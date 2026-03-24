from typing import Any, TypedDict


class AgentState(TypedDict, total=False):
    question: str
    schema_context: str
    generated_sql: str
    validated_sql: str
    query_result: list[dict[str, Any]]
    final_answer: str
    error: str
    trace: list[dict[str, Any]]