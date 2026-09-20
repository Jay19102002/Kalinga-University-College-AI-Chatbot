# pyrefly: ignore [missing-import]
from fastapi.testclient import TestClient
from app.main import app
from app.services.database import db_service

client = TestClient(app)

def test_database_stats():
    stats = db_service.get_stats()
    assert stats["total_records"] > 10000
    assert stats["courses"] >= 69
    assert stats["research_papers"] >= 4000
    assert stats["books_chapters"] >= 3000
    assert stats["patents"] >= 600
    assert stats["course_faqs"] >= 350
    assert stats["career_paths"] >= 600

def test_database_stats_api():
    response = client.get("/api/database/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total_records"] > 10000
    assert "fts_indexed_documents" in data

def test_database_search_api():
    response = client.get("/api/database/search?q=computer")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] > 0
    assert len(data["results"]) > 0

def test_research_papers_api():
    response = client.get("/api/research-papers?page=1&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] > 4000
    assert len(data["papers"]) == 5
    assert data["found"] is True

def test_books_api():
    response = client.get("/api/books?page=1&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] > 3000
    assert len(data["books"]) == 5
    assert data["found"] is True

def test_news_events_api():
    response = client.get("/api/news-events")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 30
    assert len(data["events"]) >= 30

def test_pages_api():
    response = client.get("/api/pages")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 190
    assert len(data["pages"]) >= 190

def test_catalogue_api():
    response = client.get("/api/catalogue")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 90
    assert len(data["tables"]) >= 90

def test_chat_research_query():
    payload = {"message": "Tell me about research papers in computer science", "session_id": "test_sess_research"}
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "research_papers"
    assert "scopus" in data["answer"].lower() or "research" in data["answer"].lower()
