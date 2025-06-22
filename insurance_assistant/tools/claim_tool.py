from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ClaimRequest(BaseModel):
    user_id: str

@app.post("/get_customer_claim")
def get_claim(req: ClaimRequest):
    return {
        "user_id": req.user_id,
        "status": "Approved",
        "claim_amount": "$2,000",
        "last_updated": "2025-05-26"
    }
