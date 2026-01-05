from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

from app.chat.orchestrator import chat

load_dotenv()

app = FastAPI(title="FleetOps AI Assistant", version="0.3.0")

class ChatRequest(BaseModel):
    message: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    return chat(req.message)
