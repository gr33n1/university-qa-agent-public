from app.db.repository import DatabaseRepository


def test_students_table_exists():
    repo = DatabaseRepository()
    assert repo.table_exists("students") is True


def test_can_count_students():
    repo = DatabaseRepository()
    rows = repo.execute_select("SELECT COUNT(*) AS count FROM students")
    assert len(rows) == 1
    assert rows[0]["count"] > 0


def test_join_query_databases_fall_2025():
    repo = DatabaseRepository()
    sql = """
    SELECT t.full_name AS teacher_name
    FROM course_offerings o
    JOIN teachers t ON t.teacher_id = o.teacher_id
    JOIN courses c ON c.course_id = o.course_id
    WHERE c.title = ?
      AND o.semester = ?
      AND o.academic_year = ?
    """
    rows = repo.execute_select(sql, ("Databases", "Fall", 2025))
    assert len(rows) == 1
    assert rows[0]["teacher_name"] == "Dr. Alice Smith"