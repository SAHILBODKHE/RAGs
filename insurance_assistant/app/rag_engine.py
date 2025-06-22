from llama_index.core import StorageContext, load_index_from_storage
from llama_index.llms.ollama import Ollama

def query_rag(question: str):
    llm = Ollama(model="llama3:latest")
    storage_context = StorageContext.from_defaults(persist_dir="index")
    index = load_index_from_storage(storage_context)
    query_engine = index.as_query_engine(llm=llm)
    response = query_engine.query(question)
    return str(response)
