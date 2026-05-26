from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from app.database import Base, engine
from app.models.load import Load
from app.tools.kpi_tool import total_revenue
from app.seed_data import *

from app.chat.orchestrator import chat

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FleetOps AI Assistant",
    version="0.3.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "FleetOps AI Running"}

@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    return chat(req.message)

@app.get("/revenue")
def revenue():
    return total_revenue()