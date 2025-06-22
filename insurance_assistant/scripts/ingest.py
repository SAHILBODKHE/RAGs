from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from chromadb.config import Settings

PERSIST_DIR = "index"

reader = SimpleDirectoryReader(input_dir="data", recursive=True)
docs = reader.load_data()

embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-large-en")
vector_store = ChromaVectorStore(persist_directory=PERSIST_DIR, settings=Settings(allow_reset=True))

index = VectorStoreIndex.from_documents(
    docs,
    embed_model=embed_model,
    vector_store=vector_store,
)

index.storage_context.persist()
print("✅ RAG Index built and saved.")
