from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api import health, chat, knowledge

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="NLP-Based Intelligent Student Support Chatbot REST API for Kalinga University",
    version="1.0.0"
)

# Configure CORS for local machine and all local network devices
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=r"^https?://.*$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix=settings.API_V1_STR, tags=["Health"])
app.include_router(chat.router, prefix=settings.API_V1_STR, tags=["Chat"])
app.include_router(knowledge.router, prefix=settings.API_V1_STR, tags=["Knowledge Base"])

@app.get("/")
def root():
    return {
        "message": "Welcome to Kalinga University AI Student Query Chatbot API",
        "health_check": f"{settings.API_V1_STR}/health",
        "docs": "/docs"
    }
