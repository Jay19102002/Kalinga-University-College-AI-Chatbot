from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "kalinga-ai-chatbot"
    assert data["model_loaded"] is True

def test_chat_valid_query():
    payload = {"message": "What is the admission procedure?", "session_id": "test_sess_1"}
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert data["intent"] == "admission_process"
    assert data["confidence"] > 0.30
    assert len(data["sources"]) > 0

def test_chat_empty_query():
    payload = {"message": "", "session_id": "test_sess_2"}
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 400

def test_chat_long_query():
    long_msg = "What " * 500
    payload = {"message": long_msg, "session_id": "test_sess_3"}
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "exceeds" in data["answer"].lower()
