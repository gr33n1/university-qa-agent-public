from langgraph.graph import StateGraph, END

from app.state import AgentState
from app.nodes.guard_input import guard_input_node
from app.nodes.load_schema import load_schema_node
from app.nodes.generate_sql import generate_sql_node
from app.nodes.validate_sql import validate_sql_node
from app.nodes.execute_sql import execute_sql_node
from app.nodes.repair_sql import repair_sql_node
from app.nodes.format_answer import format_answer_node


def route_after_guard_input(state: dict) -> str:
    if state.get("error"):
        return "format_answer"
    return "load_schema"


def route_after_generate_sql(state: dict) -> str:
    if state.get("error"):
        return "format_answer"
    return "validate_sql"


def route_after_validate_sql(state: dict) -> str:
    if state.get("error"):
        if state.get("repair_attempts", 0) < state.get("max_repair_attempts", 1):
            return "repair_sql"
        return "format_answer"
    return "execute_sql"


def route_after_execute_sql(state: dict) -> str:
    if state.get("error"):
        if state.get("repair_attempts", 0) < state.get("max_repair_attempts", 1):
            return "repair_sql"
        return "format_answer"
    return "format_answer"


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("guard_input", guard_input_node)
    graph.add_node("load_schema", load_schema_node)
    graph.add_node("generate_sql", generate_sql_node)
    graph.add_node("validate_sql", validate_sql_node)
    graph.add_node("execute_sql", execute_sql_node)
    graph.add_node("repair_sql", repair_sql_node)
    graph.add_node("format_answer", format_answer_node)

    graph.set_entry_point("guard_input")

    graph.add_conditional_edges(
        "guard_input",
        route_after_guard_input,
        {
            "load_schema": "load_schema",
            "format_answer": "format_answer",
        },
    )

    graph.add_edge("load_schema", "generate_sql")

    graph.add_conditional_edges(
        "generate_sql",
        route_after_generate_sql,
        {
            "validate_sql": "validate_sql",
            "format_answer": "format_answer",
        },
    )

    graph.add_conditional_edges(
        "validate_sql",
        route_after_validate_sql,
        {
            "execute_sql": "execute_sql",
            "repair_sql": "repair_sql",
            "format_answer": "format_answer",
        },
    )

    graph.add_conditional_edges(
        "execute_sql",
        route_after_execute_sql,
        {
            "repair_sql": "repair_sql",
            "format_answer": "format_answer",
        },
    )

    graph.add_edge("repair_sql", "validate_sql")
    graph.add_edge("format_answer", END)

    return graph.compile()