import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend.inference import ask_model
from backend.orders import track_order


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

APP_NAME = os.getenv("APP_NAME", "E-Commerce AI Assistant")

FRONTEND_DIR = BASE_DIR / "frontend"


app = FastAPI(title=APP_NAME)




app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Accept requests from any URL
    allow_credentials=True,
    allow_methods=["*"],      # Allow GET, POST, etc.
    allow_headers=["*"],      # Allow any headers
)



class ChatRequest(BaseModel):
    question: str



@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")



@app.post("/api/chat")
def chat(request: ChatRequest):
    return ask_model(request.question)  # Defined in backend/inference.py



@app.get("/api/order/{order_id}")
def order_status(order_id: str):
    return track_order(order_id)  # Defined in backend/orders.py