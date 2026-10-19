from fastapi import FastAPI
from backend.router import router as chatbot_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(chatbot_router)