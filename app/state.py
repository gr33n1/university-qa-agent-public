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

    repair_attempts: int
    max_repair_attempts: int
    last_error_stage: str
    last_db_error: str
    failed_sql: str