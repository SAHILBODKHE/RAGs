from fastapi import FastAPI, Request
from pydantic import BaseModel
from embed_schema import embed_schema_if_needed
from graph_traversal import get_related_tables
from llm_prompt import generate_sql_query
from query_validator import validate_sql

app = FastAPI()

class QueryRequest(BaseModel):
    user_input: str
    user_id: str

@app.post("/generate-sql/")
async def generate_sql(request: QueryRequest):
    user_query = request.user_input
    user_id = request.user_id

    seed_tables = embed_schema_if_needed(user_query)
    related_schema = get_related_tables(seed_tables, depth=2)

    sql = generate_sql_query(user_query, related_schema, user_id)

    if not validate_sql(sql, user_id, related_schema):
        return {"error": "Generated SQL failed validation"}

    return {"sql": sql}
