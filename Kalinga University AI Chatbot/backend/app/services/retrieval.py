import os
import json
from typing import Dict, Any, List, Optional
from app.config import settings
from app.services.database import db_service

class KnowledgeRetrievalService:
    def __init__(self):
        self.kb_data: Dict[str, Any] = {}
        self.source_registry: List[Dict[str, Any]] = []
        self._load_data()
        
    def _load_data(self):
        kb_files = [
            "university", "admissions", "courses", "fees", 
            "scholarships", "internships", "placements", "campus",
            "courses_detailed", "course_faqs", "career_paths",
            "internships_detailed", "mous_collaborations",
            "research_patents", "departments_detailed",
            "news_events", "page_index", "data_tables_catalogue",
            "research_papers_summary", "books_chapters_summary"
        ]
        for name in kb_files:
            file_path = os.path.join(settings.KB_DIR, f"{name}.json")
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    self.kb_data[name] = json.load(f)
                    
        if os.path.exists(settings.SOURCE_REGISTRY):
            with open(settings.SOURCE_REGISTRY, "r", encoding="utf-8") as f:
                self.source_registry = json.load(f)
                
    # pyrefly: ignore [bad-function-definition]
    def get_fee_info(self, program_name: str = None, program: str = None) -> Dict[str, Any]:
        fees_json = self.kb_data.get("fees", {})
        target_prog = program or program_name
        records = fees_json.get("fee_records", [])

        # Fallback to courses in db_service if fees_json records are empty
        if not records:
            try:
                db_courses = db_service.get_courses(limit=200)
                records = [
                    {
                        "program": c.get("program", ""),
                        "short_name": c.get("short_name", ""),
                        "level": c.get("level", ""),
                        "department": c.get("department", ""),
                        "duration": f"{c.get('tenure_years', '')} Years ({c.get('semesters', '')} Semesters)" if c.get("tenure_years") else "",
                        "tuition_fee_per_sem": f"₹{c.get('tuition_per_semester_inr', '')}" if c.get("tuition_per_semester_inr") else "",
                        "exam_fee_per_sem": f"₹{c.get('exam_fee_per_semester_inr', '1500')}" if c.get("exam_fee_per_semester_inr") else "₹1500",
                        "published_total": f"₹{c.get('total_fees_inr', '')}" if c.get("total_fees_inr") else "",
                        "official_source": c.get("url", "https://kalingauniversity.ac.in/ku-fees")
                    }
                    for c in db_courses
                ]
            except Exception:
                records = []

        if not target_prog:
            return {
                "found": True,
                "data": fees_json if fees_json else {"fee_records": records},
                "fee_records": records,
                "sources": [{"title": "Kalinga University Fee Structure (2026-27)", "url": "https://kalingauniversity.ac.in/ku-fees"}]
            }
            
        program_clean = target_prog.lower().strip()
        for record in records:
            if program_clean in record["program"].lower() or (record.get("short_name") and program_clean in record["short_name"].lower()):
                return {
                    "found": True,
                    "record": record,
                    "sources": [{"title": f"Fee details — {record['program']}", "url": record.get("official_source", "https://kalingauniversity.ac.in/ku-fees")}]
                }
                
        return {
            "found": False,
            "message": f"I don't have a reliable fee value for '{target_prog}' in my current knowledge base. Please check Kalinga University's official fee page at https://kalingauniversity.ac.in/ku-fees.",
            "sources": [{"title": "Kalinga University Official Fee Page", "url": "https://kalingauniversity.ac.in/ku-fees"}]
        }

    # pyrefly: ignore [bad-function-definition]
    def get_course_info(self, program_name: str = None, department: str = None, level: str = None, program: str = None) -> Dict[str, Any]:
        courses_json = self.kb_data.get("courses_detailed", {}).get("courses", [])
        source = {"title": "Kalinga University Academic Departments", "url": "https://kalingauniversity.ac.in/departments"}
        target_prog = program or program_name
        
        if not target_prog and not department and not level:
            return {"found": True, "data": self.kb_data.get("courses", {}), "courses": courses_json, "total": len(courses_json), "sources": [source]}
            
        matches = courses_json
        if target_prog:
            p_clean = target_prog.lower().strip()
            matches = [c for c in matches if p_clean in c["program"].lower() or p_clean in c.get("short_name", "").lower()]
        if department:
            d_clean = department.lower().strip()
            matches = [c for c in matches if d_clean in c.get("department", "").lower()]
        if level:
            l_clean = level.lower().strip()
            matches = [c for c in matches if l_clean in c.get("level", "").lower()]
        
        if matches:
            return {"found": True, "matches": matches, "total": len(matches), "sources": [source]}
        else:
            return {
                "found": False,
                "message": f"The chatbot knowledge base contains selected programs from available sources. For '{target_prog or department}', please verify full department details on the official programs page.",
                "sources": [source]
            }

    # pyrefly: ignore [bad-function-definition]
    def get_course_faqs(self, search_query: str = None, course: str = None, query: str = None) -> Dict[str, Any]:
        faqs_json = self.kb_data.get("course_faqs", {})
        source = {"title": "Kalinga University Course FAQs", "url": "https://kalingauniversity.ac.in/departments"}
        all_faqs = faqs_json.get("faqs", [])
        q_target = query or search_query
        
        if not q_target and not course:
            return {"found": True, "data": faqs_json, "faqs": all_faqs, "total": len(all_faqs), "sources": [source]}
        
        matches = all_faqs
        if course:
            c_clean = course.lower().strip()
            matches = [f for f in matches if c_clean in f.get("course", "").lower()]
        if q_target:
            q_clean = q_target.lower().strip()
            matches = [f for f in matches if q_clean in f["question"].lower() or q_clean in f.get("course", "").lower() or q_clean in f["answer"].lower()]
            
        return {"found": True, "matches": matches[:50], "total": len(matches), "sources": [source]}

    # pyrefly: ignore [bad-function-definition]
    def get_career_paths(self, search_query: str = None, course: str = None, query: str = None) -> Dict[str, Any]:
        paths_json = self.kb_data.get("career_paths", {})
        source = {"title": "Kalinga University Career Development", "url": "https://kalingauniversity.ac.in/"}
        all_paths = paths_json.get("career_paths", [])
        q_target = query or search_query
        
        if not q_target and not course:
            return {"found": True, "data": paths_json, "career_paths": all_paths, "total": len(all_paths), "sources": [source]}
        
        matches = all_paths
        if course:
            c_clean = course.lower().strip()
            matches = [p for p in matches if c_clean in p.get("course", "").lower()]
        if q_target:
            q_clean = q_target.lower().strip()
            matches = [p for p in matches if q_clean in p["course"].lower() or q_clean in p["career_path"].lower() or q_clean in p.get("description", "").lower()]
            
        return {"found": True, "matches": matches[:50], "total": len(matches), "sources": [source]}

    def get_mous_info(self, query: str = None) -> Dict[str, Any]:
        source = {"title": "Kalinga University MoUs & Collaborations", "url": "https://kalingauniversity.ac.in/academic-and-industry-collaborations"}
        if query:
            matches = db_service.get_mous(query)
            return {"found": True, "mous": matches, "total": len(matches), "sources": [source]}
        mous_json = self.kb_data.get("mous_collaborations", {})
        return {"found": True, "data": mous_json, "sources": [source]}

    def get_research_patents_info(self, query: str = None) -> Dict[str, Any]:
        source = {"title": "Kalinga University Research & Patents", "url": "https://kalingauniversity.ac.in/research"}
        if query:
            matches = db_service.get_patents(query)
            return {"found": True, "patents": matches, "total": len(matches), "sources": [source]}
        patents_json = self.kb_data.get("research_patents", {})
        return {"found": True, "data": patents_json, "sources": [source]}

    def get_research_papers_info(self, query: str = None, department: str = None, year: str = None, page: int = 1, limit: int = 20) -> Dict[str, Any]:
        source = {"title": "Kalinga University Research Publications (Scopus / UGC Care)", "url": "https://kalingauniversity.ac.in/research"}
        result = db_service.get_research_papers(query=query, department=department, year=year, page=page, limit=limit)
        result["sources"] = [source]
        result["found"] = True
        return result

    def get_books_chapters_info(self, query: str = None, department: str = None, year: str = None, page: int = 1, limit: int = 20) -> Dict[str, Any]:
        source = {"title": "Kalinga University Books & Book Chapters", "url": "https://kalingauniversity.ac.in/research"}
        result = db_service.get_books_chapters(query=query, department=department, year=year, page=page, limit=limit)
        result["sources"] = [source]
        result["found"] = True
        return result

    def get_news_events_info(self, query: str = None, category: str = None) -> Dict[str, Any]:
        source = {"title": "Kalinga University News & Events", "url": "https://kalingauniversity.ac.in/news-and-events"}
        events = db_service.get_news_events(query=query, category=category)
        return {"found": True, "events": events, "total": len(events), "sources": [source]}

    def get_page_index_info(self, query: str = None) -> Dict[str, Any]:
        source = {"title": "Kalinga University Web Directory", "url": "https://kalingauniversity.ac.in/"}
        pages = db_service.get_page_index(query=query)
        return {"found": True, "pages": pages, "total": len(pages), "sources": [source]}

    def get_data_tables_info(self, query: str = None) -> Dict[str, Any]:
        source = {"title": "Kalinga University Published Data Tables", "url": "https://kalingauniversity.ac.in/"}
        tables = db_service.get_data_tables_catalogue(query=query)
        return {"found": True, "tables": tables, "total": len(tables), "sources": [source]}

    def get_scholarship_info(self) -> Dict[str, Any]:
        sch_json = self.kb_data.get("scholarships", {})
        source = sch_json.get("source", {"title": "Kalinga University Scholarships", "url": "https://kalingauniversity.ac.in/"})
        return {"found": True, "data": sch_json, "sources": [source]}

    def get_placement_info(self, type_key: str = "general") -> Dict[str, Any]:
        pl_json = self.kb_data.get("placements", {})
        source = pl_json.get("source", {"title": "Kalinga University Training & Placements", "url": "https://kalingauniversity.ac.in/training-and-placements"})
        return {"found": True, "data": pl_json, "sources": [source]}

    def get_internship_info(self, query: str = None) -> Dict[str, Any]:
        source = {"title": "Kalinga University Campus Life & Internships", "url": "https://kalingauniversity.ac.in/campuslife"}
        if query:
            records = db_service.get_internships(query=query)
            return {"found": True, "records": records, "total": len(records), "sources": [source]}
        int_json = self.kb_data.get("internships_detailed", self.kb_data.get("internships", {}))
        return {"found": True, "data": int_json, "sources": [source]}

    def get_admission_info(self) -> Dict[str, Any]:
        adm_json = self.kb_data.get("admissions", {})
        sources = adm_json.get("sources", [{"title": "Kalinga University Admission Procedure", "url": "https://kalingauniversity.ac.in/admission-procedure"}])
        return {"found": True, "data": adm_json, "sources": sources}

kb_service = KnowledgeRetrievalService()
