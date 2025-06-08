from retriever import get_relevant_documents
from llama_model import ask_ollama
from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages

from langchain_community.chat_models import ChatOllama
from langchain.schema import HumanMessage, AIMessage

# ✅ Define the graph state schema
class State(TypedDict):
    messages: Annotated[list, add_messages]

# ✅ Initialize LangGraph builder
graph_builder = StateGraph(State)

# ✅ Initialize ChatOllama LLM
llm = ChatOllama(
    model="llama3",        # Or "llama3.2" if that's what you're running
    temperature=0.7,
    base_url="http://localhost:11434",  # Optional if default
)

# ✅ LangGraph node: performs RAG and generates LLM response
def ask(state: State) -> State:
    latest_msg = state["messages"][-1]       # HumanMessage object
    latest_input = latest_msg.content        # ✅ Proper way to access content

    docs = get_relevant_documents(latest_input)
    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
You are a helpful information assistant. Use the context below to answer the user's question.

Context:
{context}

Question: {latest_input}
Answer:
""".strip()

    response = ask_ollama(prompt)
    return {
        "messages": state["messages"] + [AIMessage(content=response)]  # ✅ Proper response format
    }

# ✅ Add nodes and edges to the graph
graph_builder.add_node("infobot", ask)
graph_builder.add_edge(START, "infobot")
graph = graph_builder.compile()

# ✅ Function to stream responses from LangGraph
def stream_graph_updates(user_input: str):
    print("Assistant:", end=" ", flush=True)
    for event in graph.stream({"messages": [HumanMessage(content=user_input)]}):
        for value in event.values():
            msg = value["messages"][-1].content
            print(msg, end="", flush=True)
    print("\n")

# ✅ REPL interface
if __name__ == "__main__":
    print("💬 LangGraph Chat Interface (type 'quit' to exit)\n")
    while True:
        try:
            user_input = input("User: ")
            if user_input.strip().lower() in {"exit", "quit", "q"}:
                print("👋 Goodbye!")
                break
            stream_graph_updates(user_input)
        except Exception as e:
            print(f"⚠️ Error: {e}")
            break
