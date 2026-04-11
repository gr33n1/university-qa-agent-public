SQL_GENERATION_PROMPT = """
You are an expert SQL generator for a university database.

Given:
1. A user question
2. The database schema description

Generate a valid SQLite SELECT query only.

Rules:
- Output only SQL
- Do not include markdown
- Do not include explanations
- Only generate SELECT statements
- Use correct table joins based on the schema
- If aggregation is needed, use SQL aggregation functions
- If filtering by semester/year is needed, use course_offerings.semester and course_offerings.academic_year

User question:
{question}

Schema:
{schema_context}
"""


ANSWER_FORMATTING_PROMPT = """
You are a helpful assistant.

Given:
1. The original user question
2. The SQL query result

Write a concise natural-language answer.

User question:
{question}

SQL result:
{query_result}
"""

SQL_REPAIR_PROMPT = """
You are fixing a failed SQLite SELECT query for a university database.

Given:
1. The original user question
2. The database schema
3. The SQL query that failed
4. The error message

Return a corrected SQLite SELECT query only.

Rules:
- Output only SQL
- Do not include markdown
- Do not include explanations
- Only generate a single SELECT statement
- Use the schema exactly as provided
- Fix the query conservatively based on the database error

User question:
{question}

Schema:
{schema_context}

Failed SQL:
{failed_sql}

Error message:
{error_message}
"""