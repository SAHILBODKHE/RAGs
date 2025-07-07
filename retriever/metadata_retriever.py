from langchain_community.vectorstores import Chroma
from embeddings import get_embedding_model

def get_chunks_by_table_names(table_names: list[str], k: int = 5):
    db = Chroma(persist_directory="db/schema", embedding_function=get_embedding_model())
    results = []
    for table in table_names:
        docs = db.similarity_search(table, k=k)
        results.extend(docs)
    return [doc.page_content for doc in results]
