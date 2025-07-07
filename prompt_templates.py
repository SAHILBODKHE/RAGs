from utils.join_extractor import extract_join_hints_from_schema

def build_sql_prompt(user_input: str, schema_chunks: list[str], user_id: str) -> str:
    raw_schema = '\n'.join(schema_chunks)
    join_hints = extract_join_hints_from_schema(raw_schema)
    join_notes = '\n'.join(f"- {hint}" for hint in join_hints)

    return f"""You are a SQL assistant.
You are given a database schema and a user request. Your task is to write a safe SQL query.

Schema:
{raw_schema}

Join Notes:
{join_notes}

Security Rule:
Only access rows where user_id = '{user_id}'

User Request:
{user_input}

SQL Query:
"""
