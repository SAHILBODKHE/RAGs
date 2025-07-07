from fastapi import FastAPI
from pydantic import BaseModel
from graph.schema_graph_builder import build_schema_graph
from graph.graph_utils import get_related_tables
from retriever.metadata_retriever import get_chunks_by_table_names
from utils.entity_linker import extract_entity_tables
from llama_model import call_llama
from prompt_templates import build_sql_prompt

app = FastAPI()

class SQLQuery(BaseModel):
    user_input: str
    user_id: str

@app.post("/generate-sql/")
def generate_sql(query: SQLQuery):
    with open("data/insurance_claims_schema.sql") as f:
        schema_sql = f.read()

    # Build schema graph once (can cache in memory if needed)
    graph = build_schema_graph(schema_sql)

    # Detect tables mentioned in user input
    all_tables = list(graph.keys())
    entity_tables = extract_entity_tables(query.user_input, all_tables)

    # Get subgraph (related tables)
    related = get_related_tables(graph, entity_tables, depth=2)

    # Retrieve schema chunks
    schema_chunks = get_chunks_by_table_names(list(related), k=1)

    # Build prompt and run model
    prompt = build_sql_prompt(query.user_input, schema_chunks, query.user_id)
    sql = call_llama(prompt)

    return {"sql": sql.strip()}
