import ollama

def generate_sql_query(user_query, schema_tables, user_id):
    context = "\n".join([f"Table: {t}" for t in schema_tables])
    prompt = f"""You are an expert SQL generator. Based on the user's question and these schema tables:
{context}
Write a SQL query to answer: {user_query}
Ensure the result is filtered with WHERE user_id = '{user_id}'.
Avoid UPDATE, DELETE, DROP. Only return the SQL query.
"""
    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]
