from pathlib import Path

from app.tracing import append_trace


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_SQL_PATH = PROJECT_ROOT / "app" / "db" / "schema.sql"


def load_schema_node(state: dict) -> dict:
    try:
        schema_sql = SCHEMA_SQL_PATH.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        state["error"] = f"Schema file not found: {SCHEMA_SQL_PATH}"
        append_trace(
            state,
            "load_schema_error",
            {"error": state["error"]},
        )
        return state
    except Exception as exc:
        state["error"] = f"Failed to load schema context: {exc}"
        append_trace(
            state,
            "load_schema_error",
            {"error": state["error"]},
        )
        return state

    state["schema_context"] = schema_sql

    append_trace(
        state,
        "load_schema",
        {
            "schema_loaded": True,
            "schema_source": str(SCHEMA_SQL_PATH),
        },
    )
    return state