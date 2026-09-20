from fastapi import APIRouter, HTTPException
from app.schemas import ChatRequest, ChatResponse
from app.services.chatbot import chatbot_service

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    if not request.message:
        raise HTTPException(status_code=400, detail="Message field cannot be empty.")
        
    session_id = request.session_id or "default_session"
    answer, intent, confidence, entities, sources = chatbot_service.process_query(request.message, session_id)
    
    return ChatResponse(
        answer=answer,
        intent=intent,
        confidence=confidence,
        entities=entities,
        sources=sources,
        session_id=session_id
    )
