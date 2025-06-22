from fastapi import FastAPI
from pydantic import BaseModel
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_ollama import ChatOllama
from langchain_core.tools import tool, InjectedToolCallId
from langchain_core.messages import ToolMessage
from langgraph.types import Command, interrupt
from typing_extensions import TypedDict, Annotated

app = FastAPI()

class State(TypedDict):
    messages: Annotated[list, add_messages]
    name: str
    birthday: str

@tool(description="Ask a human to confirm or correct name and birthday.")
def human_assistance(name: str, birthday: str, tool_call_id: Annotated[str, InjectedToolCallId]) -> str:
    return interrupt({"question": "Is this correct?", "name": name, "birthday": birthday})

llm = ChatOllama(model="llama3.2:latest").bind_tools([human_assistance])

def chatbot(state: State):
    message = llm.invoke(state["messages"])
    return {"messages": [message]}

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
tool_node = ToolNode([human_assistance])
graph_builder.add_node("tools", tool_node)
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")

graph_builder.set_entry_point("chatbot")  # ✅ this is enough


memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)
CONFIG = {"configurable": {"thread_id": "1"}}

class ResumeInput(BaseModel):
    name: str
    birthday: str

@app.post("/invoke")
def invoke_graph(input: dict):
    return graph.invoke(input, CONFIG)

@app.post("/stream")
def stream_graph(input: dict):
    events = graph.stream(input, CONFIG, stream_mode="values")
    return [e for e in events]

@app.post("/resume")
def resume(input: ResumeInput):
    cmd = Command(resume={"name": input.name, "birthday": input.birthday})
    events = graph.stream(cmd, CONFIG, stream_mode="values")
    return [e for e in events]
