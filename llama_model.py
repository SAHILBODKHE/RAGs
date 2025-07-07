from langchain.llms import Ollama

llm = Ollama(model="llama3.2", temperature=0.1)

def call_llama(prompt: str) -> str:
    return llm.predict(prompt)
