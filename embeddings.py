from langchain.embeddings import HuggingFaceEmbeddings

def get_embedding_model():
    return HuggingFaceEmbeddings(model_name="BAAI/bge-large-en")
