from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

client_app = FastAPI()

# Enable CORS for frontend access
client_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace with ["http://localhost:5500"] if desired
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class AskInput(BaseModel):
    message: str

class CorrectionInput(BaseModel):
    name: str
    birthday: str

# Route: ask LangGraph something
@client_app.post("/ask")
def ask_user(input: AskInput):
    response = requests.post("http://localhost:8000/stream", json={
        "messages": [{"role": "user", "content": input.message}]
    })
    print("Raw LangGraph response:", response.status_code, response.text)

    try:
        data = response.json()
    except Exception as e:
        return {
            "type": "error",
            "message": f"LangGraph response not JSON: {response.status_code} {response.text}"
        }

    for event in data:
        if "interrupt" in event:
            return {"type": "human_required", "data": event["interrupt"]}
        elif "messages" in event:
            return {"type": "bot_response", "data": event["messages"][-1]["content"]}

    return {"type": "unknown", "message": "No valid event found from LangGraph."}

# Route: resume execution after human correction
@client_app.post("/correction")
def correct_user(input: CorrectionInput):
    response = requests.post("http://localhost:8000/resume", json=input.dict())
    print("Correction response:", response.status_code, response.text)

    try:
        data = response.json()
    except Exception:
        return {
            "type": "error",
            "message": f"Resume failed: {response.status_code} {response.text}"
        }

    for event in data:
        if "messages" in event:
            return {"type": "bot_response", "data": event["messages"][-1]["content"]}

    return {"type": "unknown", "message": "No message returned after resume."}
