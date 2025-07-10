# semantic_search.py

import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_collection("table_embeddings")
model = SentenceTransformer("all-MiniLM-L6-v2")

def search_seed_tables(user_query: str, k: int = 3) -> list[str]:
    embedding = model.encode(user_query).tolist()
    results = collection.query(query_embeddings=[embedding], n_results=k)
    return results['ids'][0]  # List of table names
