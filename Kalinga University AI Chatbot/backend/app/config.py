import os

class Settings:
    PROJECT_NAME: str = "Kalinga University AI Student Query Chatbot"
    API_V1_STR: str = "/api"
    CONFIDENCE_THRESHOLD: float = 0.30
    MAX_MESSAGE_LENGTH: int = 2000
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "*"
    ]
    
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DATA_DIR: str = os.path.join(BASE_DIR, "data")
    KB_DIR: str = os.path.join(DATA_DIR, "knowledge_base")
    MODEL_DIR: str = os.path.join(BASE_DIR, "backend", "models")
    SOURCE_REGISTRY: str = os.path.join(DATA_DIR, "source_registry.json")
    DB_PATH: str = os.path.join(DATA_DIR, "kalinga_university.db")
    
settings = Settings()
