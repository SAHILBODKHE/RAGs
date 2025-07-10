from fastapi import FastAPI
from pydantic import BaseModel

# Internal modules
from graph_retriever.schema_parser import parse_schema_sql
from graph_retriever.graph_builder import build_join_graph
from graph_retriever.graph_traversal import expand_graph
from llm_orchestrator.sql_generator import generate_sql
from query_validation.validate import validate_sql
from semantic_search import search_seed_tables  # ✅ semantic similarity-based seed

app = FastAPI()

class SQLRequest(BaseModel):
    user_input: str
    user_id: str

@app.post("/generate-sql")
async def generate_sql_endpoint(req: SQLRequest):
    # ✅ Load schema and graph
    schema = parse_schema_sql("insurance_claims_schema.sql")
    join_graph = build_join_graph(schema)

    # ✅ Semantic table seeding
    seed_tables = search_seed_tables(req.user_input, k=3)

    # ✅ Expand graph contextually
    expanded = expand_graph(join_graph, seed_tables, depth=2)
    relevant_schema = {table: schema[table] for table in expanded}

    # ✅ Generate SQL
    sql = generate_sql(req.user_input, relevant_schema, req.user_id)

    # ✅ Validate SQL for security
    valid, error = validate_sql(sql, req.user_id, expanded)
    print("📘 Semantic Search Result (Seed Tables):", seed_tables)
    print("📘 Tables Expanded:", expanded)
    print("📘 Schema used for SQL generation:", relevant_schema.keys())
    print("📘 Generated SQL:", sql)
    print("📕 Validation Error:", error)
    if not valid:
        return {"error": error}

    return {"sql": sql}
