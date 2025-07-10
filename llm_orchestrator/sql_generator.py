import ollama
import json

def generate_sql(user_input, schema, user_id):
    schema_str = ""
    for table, cols in schema.items():
        schema_str += f"Table: {table}\nColumns: {', '.join(cols)}\n\n"

    prompt = f"""
You are an expert SQL generator.
Given the user's request and the following database schema, generate a SQL query that satisfies the request.

User request:
{user_input}

Schema:
{schema_str}

Rules:
- Only SELECT statements allowed.
- Must include `WHERE user_id = '{user_id}'`.
- Follow proper SQL syntax.

Respond with ONLY the SQL query, nothing else.
"""

    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}],
    )

    return response['message']['content'].strip()
