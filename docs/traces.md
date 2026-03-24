# Execution Trace Examples

## Trace Example 1

### User Input
How many students are enrolled in each course?

### Trace
```json
[
  {
    "step": "guard_input_passed",
    "payload": {
      "input": "How many students are enrolled in each course?",
      "normalized_question": "How many students are enrolled in each course?"
    }
  },
  {
    "step": "load_schema",
    "payload": {
      "schema_loaded": true,
      "schema_source": "C:\\Users\\sivan\\PycharmProjects\\university-qa-agent-public\\app\\db\\schema.sql"
    }
  },
  {
    "step": "generate_sql",
    "payload": {
      "question": "How many students are enrolled in each course?",
      "generated_sql": "SELECT\n  T1.course_code,\n  T1.title,\n  COUNT(T3.student_id) AS num_students_enrolled\nFROM courses AS T1\nINNER JOIN course_offerings AS T2\n  ON T1.course_id = T2.course_id\nINNER JOIN enrollments AS T3\n  ON T2.offering_id = T3.offering_id\nGROUP BY\n  T1.course_code,\n  T1.title;",
      "provider": "gemini",
      "model": "gemini-2.5-flash"
    }
  },
  {
    "step": "validate_sql",
    "payload": {
      "validated_sql": "SELECT\n  T1.course_code,\n  T1.title,\n  COUNT(T3.student_id) AS num_students_enrolled\nFROM courses AS T1\nINNER JOIN course_offerings AS T2\n  ON T1.course_id = T2.course_id\nINNER JOIN enrollments AS T3\n  ON T2.offering_id = T3.offering_id\nGROUP BY\n  T1.course_code,\n  T1.title;",
      "status": "passed"
    }
  },
  {
    "step": "execute_sql",
    "payload": {
      "sql": "SELECT\n  T1.course_code,\n  T1.title,\n  COUNT(T3.student_id) AS num_students_enrolled\nFROM courses AS T1\nINNER JOIN course_offerings AS T2\n  ON T1.course_id = T2.course_id\nINNER JOIN enrollments AS T3\n  ON T2.offering_id = T3.offering_id\nGROUP BY\n  T1.course_code,\n  T1.title;",
      "row_count": 5,
      "query_result": [
        {
          "course_code": "CS101",
          "num_students_enrolled": 4,
          "title": "Introduction to Programming"
        },
        {
          "course_code": "CS205",
          "num_students_enrolled": 5,
          "title": "Databases"
        },
        {
          "course_code": "CS310",
          "num_students_enrolled": 2,
          "title": "Algorithms"
        },
        {
          "course_code": "MATH201",
          "num_students_enrolled": 3,
          "title": "Linear Algebra"
        },
        {
          "course_code": "PHYS210",
          "num_students_enrolled": 2,
          "title": "Classical Mechanics"
        }
      ]
    }
  },
  {
    "step": "format_answer",
    "payload": {
      "final_answer": "Here's the enrollment for each course:\n\n*   **Introduction to Programming (CS101)**: 4 students\n*   **Databases (CS205)**: 5 students\n*   **Linear Algebra (MATH201)**: 3 students\n*   **Algorithms (CS310)**: 2 students\n*   **Classical Mechanics (PHYS210)**: 2 students",
      "provider": "gemini",
      "model": "gemini-2.5-flash"
    }
  }
]
```
## Trace Example 2
### User Input

DELETE FROM students

### Trace
```json
[
  {
    "step": "guard_input_blocked",
    "payload": {
      "reason": "forbidden_prefix:delete",
      "input": "DELETE FROM students"
    }
  },
  {
    "step": "format_answer_error",
    "payload": {
      "final_answer": "I couldn't complete your request: Direct SQL commands are not allowed. Please ask a natural-language question about the university database."
    }
  }
]
```

The trace follows the required flow:
User Input → LangGraph Nodes → SQL → DB Results → Final Answer
