from retriever import get_relevant_documents
from llama_model import ask_ollama

def ask(query):
    docs = get_relevant_documents(query)
    context = "\n\n".join([doc.page_content for doc in docs])
    
    prompt = f"""
You are a helpful medical assistant. Use the context below to answer the user's question.

Context:
{context}

Question: {query}
Answer:
"""
    response = ask_ollama(prompt.strip())
    print("\n💬 Answer:", response)

if __name__ == "__main__":
    while True:
        q = input("\n❓ Ask a question: ")
        ask(q)
