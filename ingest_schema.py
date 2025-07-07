from langchain.docstore.document import Document
from langchain_community.vectorstores import Chroma
from embeddings import get_embedding_model

def ingest_schema():
    with open("data/insurance_claims_schema.sql", "r") as f:
        raw = f.read()

    chunks = raw.split("CREATE TABLE")
    docs = []
    for chunk in chunks:
        if not chunk.strip():
            continue
        chunk_text = "CREATE TABLE " + chunk.strip()
        table_name = chunk.strip().split()[0].strip("()").lower()
        docs.append(Document(page_content=chunk_text, metadata={"table": table_name}))

    db = Chroma.from_documents(docs, get_embedding_model(), persist_directory="db/schema")
    db.persist()
    print("✅ Ingested", len(docs), "tables.")

if __name__ == "__main__":
    ingest_schema()
