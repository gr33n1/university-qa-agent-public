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