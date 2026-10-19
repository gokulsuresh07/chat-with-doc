from fastapi import APIRouter
from backend.chatbot import service
from backend.chatbot.schema import ChatPayload

router = APIRouter()

@router.get("/store-data")
def store_document_data():
    return service.store_data_from_doc()

@router.post("/chat")
def chat(payload: ChatPayload):
    return service.chat_with_data(payload)

