import os
import sqlite3
import re
from typing import Dict, Any, List, Optional
from app.config import settings

class DatabaseService:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or settings.DB_PATH

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def get_stats(self) -> Dict[str, Any]:
        tables = [
            "courses", "course_faqs", "career_paths", "training_internships",
            "mous_collaborations", "patents", "research_papers", "books_chapters",
            "news_events", "page_index", "data_tables_catalogue", "departments"
        ]
        stats = {}
        total = 0
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                for table in tables:
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        cnt = cursor.fetchone()[0]
                        stats[table] = cnt
                        total += cnt
                    except sqlite3.OperationalError:
                        stats[table] = 0
                
                try:
                    cursor.execute("SELECT COUNT(*) FROM fts_knowledge")
                    stats["fts_indexed_documents"] = cursor.fetchone()[0]
                except sqlite3.OperationalError:
                    stats["fts_indexed_documents"] = 0
                    
            stats["total_records"] = total
        except Exception as e:
            stats = {"error": str(e), "total_records": 0}
        return stats

    def search_global(self, query: str, entity_type: Optional[str] = None, limit: int = 25) -> List[Dict[str, Any]]:
        if not query or not query.strip():
            return []
        
        q_clean = query.strip()
        results = []
        
        # Format query for SQLite FTS5
        # Remove special characters to avoid FTS syntax errors
        fts_term = re.sub(r'[^\w\s]', ' ', q_clean)
        words = [w for w in fts_term.split() if w]
        if not words:
            return []
        fts_query = " ".join([f'"{w}"*' for w in words])
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                if entity_type:
                    cursor.execute("""
                        SELECT entity_type, title, subtitle, content, source_url
                        FROM fts_knowledge
                        WHERE entity_type = ? AND fts_knowledge MATCH ?
                        ORDER BY rank
                        LIMIT ?
                    """, (entity_type, fts_query, limit))
                else:
                    cursor.execute("""
                        SELECT entity_type, title, subtitle, content, source_url
                        FROM fts_knowledge
                        WHERE fts_knowledge MATCH ?
                        ORDER BY rank
                        LIMIT ?
                    """, (fts_query, limit))
                
                for row in cursor.fetchall():
                    results.append({
                        "entity_type": row["entity_type"],
                        "title": row["title"],
                        "subtitle": row["subtitle"],
                        "content": row["content"],
                        "source_url": row["source_url"]
                    })
        except sqlite3.OperationalError:
            # Fallback to standard LIKE search across courses and faqs if FTS fails
            like_term = f"%{q_clean}%"
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT 'course' as entity_type, program as title, department as subtitle, specializations as content, url as source_url
                    FROM courses
                    WHERE program LIKE ? OR short_name LIKE ? OR department LIKE ?
                    LIMIT ?
                """, (like_term, like_term, like_term, limit))
                for row in cursor.fetchall():
                    results.append(dict(row))
        return results

    def get_courses(self, program: Optional[str] = None, department: Optional[str] = None, level: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM courses WHERE 1=1"
            params = []
            if program:
                query += " AND (LOWER(program) LIKE ? OR LOWER(short_name) LIKE ?)"
                p = f"%{program.lower().strip()}%"
                params.extend([p, p])
            if department:
                query += " AND LOWER(department) LIKE ?"
                params.append(f"%{department.lower().strip()}%")
            if level:
                query += " AND LOWER(level) = ?"
                params.append(level.lower().strip())
            query += " ORDER BY level, program LIMIT ?"
            params.append(limit)
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    def get_research_papers(self, query: Optional[str] = None, department: Optional[str] = None, year: Optional[str] = None, page: int = 1, limit: int = 20) -> Dict[str, Any]:
        offset = max(0, (page - 1) * limit)
        with self.get_connection() as conn:
            cursor = conn.cursor()
            base_sql = "FROM research_papers WHERE 1=1"
            params = []
            
            if query:
                base_sql += " AND (LOWER(title) LIKE ? OR LOWER(authors) LIKE ? OR LOWER(journal) LIKE ?)"
                q = f"%{query.lower().strip()}%"
                params.extend([q, q, q])
            if department:
                base_sql += " AND LOWER(department) LIKE ?"
                params.append(f"%{department.lower().strip()}%")
            if year:
                base_sql += " AND year = ?"
                params.append(year.strip())
                
            cursor.execute(f"SELECT COUNT(*) {base_sql}", params)
            total = cursor.fetchone()[0]
            
            query_sql = f"SELECT * {base_sql} ORDER BY year DESC, id ASC LIMIT ? OFFSET ?"
            query_params = list(params) + [limit, offset]
            cursor.execute(query_sql, query_params)
            rows = cursor.fetchall()
            
            return {
                "total": total,
                "page": page,
                "limit": limit,
                "total_pages": (total + limit - 1) // limit if total > 0 else 1,
                "papers": [dict(r) for r in rows]
            }

    def get_books_chapters(self, query: Optional[str] = None, department: Optional[str] = None, year: Optional[str] = None, page: int = 1, limit: int = 20) -> Dict[str, Any]:
        offset = max(0, (page - 1) * limit)
        with self.get_connection() as conn:
            cursor = conn.cursor()
            base_sql = "FROM books_chapters WHERE 1=1"
            params = []
            
            if query:
                base_sql += " AND (LOWER(title) LIKE ? OR LOWER(author) LIKE ? OR LOWER(publisher) LIKE ?)"
                q = f"%{query.lower().strip()}%"
                params.extend([q, q, q])
            if department:
                base_sql += " AND LOWER(department) LIKE ?"
                params.append(f"%{department.lower().strip()}%")
            if year:
                base_sql += " AND year = ?"
                params.append(year.strip())
                
            cursor.execute(f"SELECT COUNT(*) {base_sql}", params)
            total = cursor.fetchone()[0]
            
            query_sql = f"SELECT * {base_sql} ORDER BY year DESC, id ASC LIMIT ? OFFSET ?"
            query_params = list(params) + [limit, offset]
            cursor.execute(query_sql, query_params)
            rows = cursor.fetchall()
            
            return {
                "total": total,
                "page": page,
                "limit": limit,
                "total_pages": (total + limit - 1) // limit if total > 0 else 1,
                "books": [dict(r) for r in rows]
            }

    def get_news_events(self, query: Optional[str] = None, category: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            sql = "SELECT * FROM news_events WHERE 1=1"
            params = []
            if query:
                sql += " AND (LOWER(heading) LIKE ? OR LOWER(summary) LIKE ?)"
                q = f"%{query.lower().strip()}%"
                params.extend([q, q])
            if category:
                sql += " AND LOWER(category) = ?"
                params.append(category.lower().strip())
            sql += " ORDER BY id ASC LIMIT ?"
            params.append(limit)
            cursor.execute(sql, params)
            return [dict(r) for r in cursor.fetchall()]

    def get_page_index(self, query: Optional[str] = None, limit: int = 250) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            sql = "SELECT * FROM page_index WHERE 1=1"
            params = []
            if query:
                sql += " AND (LOWER(slug) LIKE ? OR LOWER(title) LIKE ? OR LOWER(meta_description) LIKE ?)"
                q = f"%{query.lower().strip()}%"
                params.extend([q, q, q])
            sql += " ORDER BY title ASC LIMIT ?"
            params.append(limit)
            cursor.execute(sql, params)
            return [dict(r) for r in cursor.fetchall()]

    def get_data_tables_catalogue(self, query: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            sql = "SELECT * FROM data_tables_catalogue WHERE 1=1"
            params = []
            if query:
                sql += " AND (LOWER(title) LIKE ? OR LOWER(headers) LIKE ?)"
                q = f"%{query.lower().strip()}%"
                params.extend([q, q])
            sql += " ORDER BY title ASC LIMIT ?"
            params.append(limit)
            cursor.execute(sql, params)
            return [dict(r) for r in cursor.fetchall()]

    def get_faqs(self, query: Optional[str] = None, course: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            sql = "SELECT * FROM course_faqs WHERE 1=1"
            params = []
            if query:
                sql += " AND (LOWER(question) LIKE ? OR LOWER(answer) LIKE ?)"
                q = f"%{query.lower().strip()}%"
                params.extend([q, q])
            if course:
                sql += " AND LOWER(course) LIKE ?"
                params.append(f"%{course.lower().strip()}%")
            sql += " LIMIT ?"
            params.append(limit)
            cursor.execute(sql, params)
            return [dict(r) for r in cursor.fetchall()]

    def get_career_paths(self, query: Optional[str] = None, course: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            sql = "SELECT * FROM career_paths WHERE 1=1"
            params = []
            if query:
                sql += " AND (LOWER(career_path) LIKE ? OR LOWER(description) LIKE ?)"
                q = f"%{query.lower().strip()}%"
                params.extend([q, q])
            if course:
                sql += " AND LOWER(course) LIKE ?"
                params.append(f"%{course.lower().strip()}%")
            sql += " LIMIT ?"
            params.append(limit)
            cursor.execute(sql, params)
            return [dict(r) for r in cursor.fetchall()]

    def get_patents(self, query: Optional[str] = None, status: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            sql = "SELECT * FROM patents WHERE 1=1"
            params = []
            if query:
                sql += " AND (LOWER(topic) LIKE ? OR LOWER(inventor) LIKE ?)"
                q = f"%{query.lower().strip()}%"
                params.extend([q, q])
            if status:
                sql += " AND LOWER(status) LIKE ?"
                params.append(f"%{status.lower().strip()}%")
            sql += " LIMIT ?"
            params.append(limit)
            cursor.execute(sql, params)
            return [dict(r) for r in cursor.fetchall()]

    def get_internships(self, query: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            sql = "SELECT * FROM training_internships WHERE 1=1"
            params = []
            if query:
                sql += " AND (LOWER(company) LIKE ? OR LOWER(student_name) LIKE ? OR LOWER(course_name) LIKE ?)"
                q = f"%{query.lower().strip()}%"
                params.extend([q, q, q])
            sql += " LIMIT ?"
            params.append(limit)
            cursor.execute(sql, params)
            return [dict(r) for r in cursor.fetchall()]

    def get_mous(self, query: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            sql = "SELECT * FROM mous_collaborations WHERE 1=1"
            params = []
            if query:
                sql += " AND (LOWER(partner) LIKE ? OR LOWER(faculty) LIKE ? OR LOWER(category) LIKE ?)"
                q = f"%{query.lower().strip()}%"
                params.extend([q, q, q])
            sql += " LIMIT ?"
            params.append(limit)
            cursor.execute(sql, params)
            return [dict(r) for r in cursor.fetchall()]

db_service = DatabaseService()
