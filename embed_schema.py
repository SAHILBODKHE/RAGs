import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from graph_retriever.schema_parser import parse_schema_sql

# ✅ Load model for embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

import chromadb

import chromadb

client = chromadb.PersistentClient(path="./chroma_db")


# ✅ Create or get the collection
collection = client.get_or_create_collection("table_embeddings")

# ✅ Parse schema file
schema = parse_schema_sql("insurance_claims_schema.sql")

# ✅ Prepare and embed each table description
for table, columns in schema.items():
    col_names = ", ".join(columns.keys())
    desc = f"Table '{table}' with columns: {col_names}"
    embedding = model.encode(desc).tolist()

    collection.add(
        documents=[desc],
        metadatas=[{"table": table}],
        ids=[table],
        embeddings=[embedding]
    )

print("✅ All table embeddings saved to ChromaDB!")
