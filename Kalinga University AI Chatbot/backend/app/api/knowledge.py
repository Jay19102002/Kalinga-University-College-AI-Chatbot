from fastapi import APIRouter, Query
from typing import Optional
from app.services.retrieval import kb_service
from app.services.chatbot import chatbot_service
from app.services.database import db_service

router = APIRouter()

@router.get("/database/stats")
def get_database_stats():
    """Return live record counts across the complete Kalinga University database."""
    return db_service.get_stats()

@router.get("/database/search")
def search_database(
    q: str = Query(..., min_length=1, description="Search query string"),
    entity_type: Optional[str] = Query(None, description="Filter by entity type (course, faq, career_path, research_paper, book_chapter, patent, news_event, internship, mou, page)"),
    limit: int = Query(25, ge=1, le=100)
):
    """Full-text search (FTS5) across the entire Kalinga University Knowledge Base."""
    results = db_service.search_global(query=q, entity_type=entity_type, limit=limit)
    return {
        "query": q,
        "entity_type": entity_type,
        "count": len(results),
        "results": results
    }

@router.get("/intents")
def get_intents():
    return chatbot_service.intents_data.get("intents", [])

@router.get("/courses")
def get_courses(
    program: Optional[str] = None,
    department: Optional[str] = None,
    level: Optional[str] = None
):
    return kb_service.get_course_info(program=program, department=department, level=level)

@router.get("/fees")
def get_fees(program: Optional[str] = None):
    return kb_service.get_fee_info(program=program)

@router.get("/scholarships")
def get_scholarships():
    return kb_service.get_scholarship_info()

@router.get("/internships")
def get_internships(query: Optional[str] = None):
    return kb_service.get_internship_info(query=query)

@router.get("/placements")
def get_placements():
    return kb_service.get_placement_info()

@router.get("/faqs")
def get_faqs(query: Optional[str] = None, course: Optional[str] = None):
    return kb_service.get_course_faqs(search_query=query, course=course)

@router.get("/career_paths")
def get_career_paths(query: Optional[str] = None, course: Optional[str] = None):
    return kb_service.get_career_paths(search_query=query, course=course)

@router.get("/mous")
def get_mous(query: Optional[str] = None):
    return kb_service.get_mous_info(query=query)

@router.get("/patents")
def get_patents(query: Optional[str] = None):
    return kb_service.get_research_patents_info(query=query)

@router.get("/research-papers")
def get_research_papers(
    query: Optional[str] = None,
    department: Optional[str] = None,
    year: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    return kb_service.get_research_papers_info(query=query, department=department, year=year, page=page, limit=limit)

@router.get("/books")
def get_books_chapters(
    query: Optional[str] = None,
    department: Optional[str] = None,
    year: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    return kb_service.get_books_chapters_info(query=query, department=department, year=year, page=page, limit=limit)

@router.get("/news-events")
def get_news_events(query: Optional[str] = None, category: Optional[str] = None):
    return kb_service.get_news_events_info(query=query, category=category)

@router.get("/pages")
def get_page_index(query: Optional[str] = None):
    return kb_service.get_page_index_info(query=query)

@router.get("/catalogue")
def get_data_tables_catalogue(query: Optional[str] = None):
    return kb_service.get_data_tables_info(query=query)
