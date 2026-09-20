from fastapi import APIRouter
from app.schemas import HealthResponse
from app.services.chatbot import chatbot_service

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
def health_check():
    model_loaded = (chatbot_service.vectorizer is not None and chatbot_service.classifier is not None)
    intents_count = len(chatbot_service.intents_data.get("intents", []))
    
    return HealthResponse(
        status="ok",
        service="kalinga-ai-chatbot",
        model_loaded=model_loaded,
        intents_count=intents_count
    )
