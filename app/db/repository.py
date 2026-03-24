from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "app" / "db" / "university.db"


class DatabaseRepository:
    def __init__(self, db_path: str | Path | None = None) -> None:
        self.db_path = Path(db_path) if db_path else DB_PATH

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def execute_select(self, sql: str, params: tuple[Any, ...] | None = None) -> list[dict[str, Any]]:
        if not sql.strip().lower().startswith("select"):
            raise ValueError("Only SELECT queries are allowed in execute_select().")

        with self._connect() as conn:
            cursor = conn.execute(sql, params or ())
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def execute_script(self, sql_script: str) -> None:
        with self._connect() as conn:
            conn.executescript(sql_script)
            conn.commit()

    def table_exists(self, table_name: str) -> bool:
        sql = """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table' AND name = ?
        """
        rows = self.execute_raw(sql, (table_name,))
        return len(rows) > 0

    def execute_raw(self, sql: str, params: tuple[Any, ...] | None = None) -> list[dict[str, Any]]:
        with self._connect() as conn:
            cursor = conn.execute(sql, params or ())
            rows = cursor.fetchall()
            return [dict(row) for row in rows]