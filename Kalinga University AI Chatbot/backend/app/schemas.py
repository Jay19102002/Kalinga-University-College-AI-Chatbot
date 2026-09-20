from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ChatRequest(BaseModel):
    message: str = Field(..., description="Student query string", example="What is the fee for BBA?")
    session_id: Optional[str] = Field(None, description="Optional session identifier for context tracking")

class SourceItem(BaseModel):
    title: str
    url: str
    type: Optional[str] = "official"

class ChatResponse(BaseModel):
    answer: str
    intent: str
    confidence: float
    entities: Dict[str, Any] = {}
    sources: List[SourceItem] = []
    session_id: str

class HealthResponse(BaseModel):
    status: str
    service: str
    model_loaded: bool
    intents_count: int
