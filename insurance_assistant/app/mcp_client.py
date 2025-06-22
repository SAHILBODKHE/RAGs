import requests

def call_mcp_tool(user_message: str, user_id: str):
    if "claim" in user_message.lower():
        res = requests.post(
            "http://localhost:8001/get_customer_claim",
            json={"user_id": user_id}
        )
        return res.json()
    return {"error": "No matching tool"}
