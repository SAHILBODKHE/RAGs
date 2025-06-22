from fastapi import FastAPI
from pydantic import BaseModel
from app.rag_engine import query_rag
from app.mcp_client import call_mcp_tool

app = FastAPI()

class Query(BaseModel):
    message: str
    user_id: str

@app.post("/ask")
def ask(query: Query):
    msg = query.message.lower()

    if "policy" in msg or "coverage" in msg or "covid" in msg:
        return {"source": "RAG", "response": query_rag(query.message)}

    return {"source": "MCP", "response": call_mcp_tool(query.message, query.user_id)}
