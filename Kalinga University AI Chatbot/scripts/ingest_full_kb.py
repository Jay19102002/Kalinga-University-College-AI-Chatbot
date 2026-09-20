import os
import json
import csv
import re
import sqlite3
from typing import List, Dict, Any

KB_SOURCE_DIR = "Knowledge Base"
KB_TARGET_DIR = os.path.join("data", "knowledge_base")
DB_PATH = os.path.join("data", "kalinga_university.db")

def clean_html(text: str) -> str:
    if not text:
        return ""
    clean = re.sub(r"<[^>]+>", "", text)
    return " ".join(clean.split()).strip()

def setup_sqlite_tables(conn: sqlite3.Connection):
    cursor = conn.cursor()
    
    # 1. Courses
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        program TEXT NOT NULL,
        short_name TEXT,
        level TEXT,
        department TEXT,
        url TEXT,
        specializations TEXT,
        tenure_years TEXT,
        semesters TEXT,
        tuition_per_semester_inr TEXT,
        exam_fee_per_semester_inr TEXT,
        total_fees_inr TEXT,
        lateral_entry_total_inr TEXT,
        clubs TEXT,
        fee_note TEXT
    );
    """)
    
    # 2. Course FAQs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS course_faqs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course TEXT NOT NULL,
        question TEXT NOT NULL,
        answer TEXT NOT NULL
    );
    """)
    
    # 3. Career Paths
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS career_paths (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course TEXT NOT NULL,
        career_path TEXT NOT NULL,
        description TEXT
    );
    """)
    
    # 4. Training & Internships
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS training_internships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session TEXT,
        student_name TEXT,
        course_code TEXT,
        course_name TEXT,
        company TEXT
    );
    """)
    
    # 5. MoUs & Collaborations
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mous_collaborations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        partner TEXT NOT NULL,
        start_date TEXT,
        end_date TEXT,
        location TEXT,
        country TEXT,
        category TEXT,
        faculty TEXT
    );
    """)
    
    # 6. Patents
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        inventor TEXT,
        faculty TEXT,
        topic TEXT NOT NULL,
        pub_date TEXT,
        app_no TEXT,
        status TEXT
    );
    """)
    
    # 7. Research Papers
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS research_papers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        authors TEXT,
        department TEXT,
        journal TEXT,
        year TEXT,
        issn TEXT,
        url TEXT,
        indexing TEXT
    );
    """)
    
    # 8. Books & Chapters
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books_chapters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        author TEXT,
        department TEXT,
        title TEXT NOT NULL,
        conference TEXT,
        proceeding_title TEXT,
        nat_intl TEXT,
        year TEXT,
        isbn TEXT,
        institute TEXT,
        publisher TEXT
    );
    """)
    
    # 9. News & Events
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS news_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        heading TEXT NOT NULL,
        category TEXT,
        department TEXT,
        url TEXT,
        summary TEXT,
        reading_time TEXT
    );
    """)
    
    # 10. Page Index
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS page_index (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        slug TEXT NOT NULL,
        url TEXT NOT NULL,
        title TEXT,
        meta_description TEXT,
        content_chars INTEGER
    );
    """)
    
    # 11. Data Tables Catalogue
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS data_tables_catalogue (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_id TEXT,
        title TEXT NOT NULL,
        category TEXT,
        department TEXT,
        rows_count INTEGER,
        columns_count INTEGER,
        headers TEXT,
        updated_at TEXT
    );
    """)
    
    # 12. Programmes by Faculty
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS programmes_faculty (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        department TEXT NOT NULL,
        programme TEXT,
        description TEXT
    );
    """)
    
    # 13. Departments
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS departments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        slug TEXT,
        description TEXT,
        programs_count INTEGER
    );
    """)

    # FTS5 Full Text Search Table
    cursor.execute("DROP TABLE IF EXISTS fts_knowledge;")
    cursor.execute("""
    CREATE VIRTUAL TABLE fts_knowledge USING fts5(
        entity_type,
        title,
        subtitle,
        content,
        source_url
    );
    """)
    
    conn.commit()

def ingest_courses_detailed(conn: sqlite3.Connection):
    csv_path = os.path.join(KB_SOURCE_DIR, "KU — Courses with fees (69).csv")
    courses = []
    cursor = conn.cursor()
    cursor.execute("DELETE FROM courses;")
    
    if os.path.exists(csv_path):
        with open(csv_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                p = row.get("name", "").strip()
                if not p:
                    continue
                short_name = row.get("short_name", "").strip()
                level = row.get("level", "").strip()
                dept = row.get("department", "").strip()
                url = row.get("url", "").strip()
                specs = "; ".join([s.strip() for s in row.get("specializations", "").split(";") if s.strip()])
                tenure = row.get("tenure_years", "").strip()
                sems = row.get("semesters", "").strip()
                tuition = row.get("tuition_per_semester_inr", "").strip()
                exam = row.get("exam_fee_per_semester_inr", "").strip()
                total = row.get("total_fees_inr", "").strip()
                lateral = row.get("lateral_entry_total_inr", "").strip()
                clubs = row.get("clubs", "").strip()
                fee_note = row.get("fee_note", "").strip()
                
                courses.append({
                    "program": p,
                    "short_name": short_name,
                    "level": level,
                    "department": dept,
                    "url": url,
                    "specializations": [s.strip() for s in specs.split(";") if s.strip()],
                    "tenure_years": tenure,
                    "semesters": sems,
                    "tuition_per_semester_inr": tuition,
                    "exam_fee_per_semester_inr": exam,
                    "total_fees_inr": total,
                    "lateral_entry_total_inr": lateral,
                    "clubs": clubs,
                    "fee_note": fee_note
                })
                
                cursor.execute("""
                INSERT INTO courses (
                    program, short_name, level, department, url,
                    specializations, tenure_years, semesters, tuition_per_semester_inr,
                    exam_fee_per_semester_inr, total_fees_inr, lateral_entry_total_inr,
                    clubs, fee_note
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (p, short_name, level, dept, url, specs, tenure, sems, tuition, exam, total, lateral, clubs, fee_note))
                
                cursor.execute("""
                INSERT INTO fts_knowledge (entity_type, title, subtitle, content, source_url)
                VALUES (?, ?, ?, ?, ?)
                """, (
                    "course",
                    f"{p} ({short_name})" if short_name else p,
                    f"{dept} • {level} Program",
                    f"Duration: {tenure} Years ({sems} Semesters). Tuition fee: ₹{tuition}/sem, Exam fee: ₹{exam}/sem. Total: ₹{total}. Specializations: {specs}. Fee note: {fee_note}",
                    url or "https://kalingauniversity.ac.in/departments"
                ))
    
    target_path = os.path.join(KB_TARGET_DIR, "courses_detailed.json")
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump({"total": len(courses), "courses": courses}, f, indent=2)
    conn.commit()
    print(f"[OK] Ingested {len(courses)} courses -> SQLite & {target_path}")
    return courses

def ingest_course_faqs(conn: sqlite3.Connection):
    csv_path = os.path.join(KB_SOURCE_DIR, "KU — Course FAQs (355).csv")
    faqs = []
    cursor = conn.cursor()
    cursor.execute("DELETE FROM course_faqs;")
    
    if os.path.exists(csv_path):
        with open(csv_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                course = row.get("course", "").strip()
                q = clean_html(row.get("question", "").strip())
                a = clean_html(row.get("answer", "").strip())
                if q and a:
                    faqs.append({"course": course, "question": q, "answer": a})
                    cursor.execute("INSERT INTO course_faqs (course, question, answer) VALUES (?, ?, ?)", (course, q, a))
                    cursor.execute("""
                    INSERT INTO fts_knowledge (entity_type, title, subtitle, content, source_url)
                    VALUES (?, ?, ?, ?, ?)
                    """, ("faq", q, course, a, "https://kalingauniversity.ac.in/departments"))
                    
    target_path = os.path.join(KB_TARGET_DIR, "course_faqs.json")
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump({"total": len(faqs), "faqs": faqs}, f, indent=2)
    conn.commit()
    print(f"[OK] Ingested {len(faqs)} course FAQs -> SQLite & {target_path}")
    return faqs

def ingest_career_paths(conn: sqlite3.Connection):
    csv_path = os.path.join(KB_SOURCE_DIR, "KU — Career paths by course (621).csv")
    career_paths = []
    cursor = conn.cursor()
    cursor.execute("DELETE FROM career_paths;")
    
    if os.path.exists(csv_path):
        with open(csv_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                course = row.get("course", "").strip()
                path = row.get("career_path", "").strip()
                desc = clean_html(row.get("description", "").strip())
                if course and path:
                    career_paths.append({"course": course, "career_path": path, "description": desc})
                    cursor.execute("INSERT INTO career_paths (course, career_path, description) VALUES (?, ?, ?)", (course, path, desc))
                    cursor.execute("""
                    INSERT INTO fts_knowledge (entity_type, title, subtitle, content, source_url)
                    VALUES (?, ?, ?, ?, ?)
                    """, ("career_path", path, f"Career opportunity for {course}", desc, "https://kalingauniversity.ac.in/"))
                    
    target_path = os.path.join(KB_TARGET_DIR, "career_paths.json")
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump({"total": len(career_paths), "career_paths": career_paths}, f, indent=2)
    conn.commit()
    print(f"[OK] Ingested {len(career_paths)} career paths -> SQLite & {target_path}")
    return career_paths

def ingest_internships_detailed(conn: sqlite3.Connection):
    csv_path = os.path.join(KB_SOURCE_DIR, "KU — Training and internships (649).csv")
    records = []
    cursor = conn.cursor()
    cursor.execute("DELETE FROM training_internships;")
    
    if os.path.exists(csv_path):
        with open(csv_path, "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            next(reader, None) # skip header
            for row in reader:
                if not row or len(row) < 7:
                    continue
                session = row[0].strip()
                code = row[3].strip() if len(row) > 3 else ""
                name_course = row[4].strip() if len(row) > 4 else ""
                student = row[5].strip() if len(row) > 5 else ""
                company = row[6].strip() if len(row) > 6 else ""
                if not company and len(row) > 7:
                    company = row[7].strip()
                if company or student or name_course:
                    records.append({
                        "session": session,
                        "student": student,
                        "course_code": code,
                        "course": name_course,
                        "company": company
                    })
                    cursor.execute("""
                    INSERT INTO training_internships (session, student_name, course_code, course_name, company)
                    VALUES (?, ?, ?, ?, ?)
                    """, (session, student, code, name_course, company))
                    if company and student:
                        cursor.execute("""
                        INSERT INTO fts_knowledge (entity_type, title, subtitle, content, source_url)
                        VALUES (?, ?, ?, ?, ?)
                        """, ("internship", f"Internship at {company}", f"{student} ({name_course})", f"Session: {session}. Program: {code} - {name_course}", "https://kalingauniversity.ac.in/training-and-placements"))
                        
    target_path = os.path.join(KB_TARGET_DIR, "internships_detailed.json")
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump({"total": len(records), "records": records}, f, indent=2)
    conn.commit()
    print(f"[OK] Ingested {len(records)} internship records -> SQLite & {target_path}")
    return records

def ingest_mous_collaborations(conn: sqlite3.Connection):
    csv_path = os.path.join(KB_SOURCE_DIR, "KU — MoUs and collaborations (438).csv")
    mous = []
    cursor = conn.cursor()
    cursor.execute("DELETE FROM mous_collaborations;")
    
    if os.path.exists(csv_path):
        with open(csv_path, "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if not row or len(row) < 5:
                    continue
                start_date = row[2].strip() if len(row) > 2 else ""
                end_date = row[3].strip() if len(row) > 3 else ""
                partner = row[4].strip() if len(row) > 4 else ""
                location = row[5].strip() if len(row) > 5 else ""
                country = row[6].strip() if len(row) > 6 else ""
                category = row[7].strip() if len(row) > 7 else ""
                faculty = row[8].strip() if len(row) > 8 else ""
                if partner:
                    mous.append({
                        "partner": partner,
                        "start_date": start_date,
                        "end_date": end_date,
                        "location": location,
                        "country": country,
                        "category": category,
                        "faculty": faculty
                    })
                    cursor.execute("""
                    INSERT INTO mous_collaborations (partner, start_date, end_date, location, country, category, faculty)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (partner, start_date, end_date, location, country, category, faculty))
                    cursor.execute("""
                    INSERT INTO fts_knowledge (entity_type, title, subtitle, content, source_url)
                    VALUES (?, ?, ?, ?, ?)
                    """, ("mou", partner, f"{category} • {faculty}", f"MoU Duration: {start_date} to {end_date}. Location: {location}, {country}. Faculty: {faculty}", "https://kalingauniversity.ac.in/academic-and-industry-collaborations"))
                    
    target_path = os.path.join(KB_TARGET_DIR, "mous_collaborations.json")
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump({"total": len(mous), "mous": mous}, f, indent=2)
    conn.commit()
    print(f"[OK] Ingested {len(mous)} MoUs -> SQLite & {target_path}")
    return mous

def ingest_research_patents(conn: sqlite3.Connection):
    csv_path = os.path.join(KB_SOURCE_DIR, "KU — Patents (600).csv")
    patents = []
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patents;")
    
    if os.path.exists(csv_path):
        with open(csv_path, "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if not row or len(row) < 6:
                    continue
                inventor = row[2].strip() if len(row) > 2 else ""
                faculty = row[3].strip() if len(row) > 3 else ""
                topic = clean_html(row[4].strip()) if len(row) > 4 else ""
                pub_date = row[5].strip() if len(row) > 5 else ""
                app_no = row[6].strip() if len(row) > 6 else ""
                status = row[7].strip() if len(row) > 7 else ""
                if topic:
                    patents.append({
                        "inventor": inventor,
                        "faculty": faculty,
                        "topic": topic,
                        "date": pub_date,
                        "app_no": app_no,
                        "status": status
                    })
                    cursor.execute("""
                    INSERT INTO patents (inventor, faculty, topic, pub_date, app_no, status)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """, (inventor, faculty, topic, pub_date, app_no, status))
                    cursor.execute("""
                    INSERT INTO fts_knowledge (entity_type, title, subtitle, content, source_url)
                    VALUES (?, ?, ?, ?, ?)
                    """, ("patent", topic, f"Inventor: {inventor} • {faculty}", f"Status: {status}. App No: {app_no}. Published Date: {pub_date}.", "https://kalingauniversity.ac.in/research"))
                    
    target_path = os.path.join(KB_TARGET_DIR, "research_patents.json")
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump({"total": len(patents), "patents": patents}, f, indent=2)
    conn.commit()
    print(f"[OK] Ingested {len(patents)} patents -> SQLite & {target_path}")
    return patents

def ingest_research_papers(conn: sqlite3.Connection):
    csv_path = os.path.join(KB_SOURCE_DIR, "KU — Research papers (4,869).csv")
    papers = []
    cursor = conn.cursor()
    cursor.execute("DELETE FROM research_papers;")
    
    if os.path.exists(csv_path):
        with open(csv_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = clean_html(row.get("Title of paper", "").strip())
                authors = row.get("Name of the author/s", "").strip()
                dept = row.get("Department of the teacher", "").strip()
                journal = row.get("Name of journal", "").strip()
                year = row.get("Year of publication", "").strip()
                issn = row.get("ISSN number", "").strip()
                url = row.get("Link to the recognition in UGC enlistment of the Journal", "").strip()
                indexing = row.get("Is it listed in  UGC Care  list/Scopus/Web of Science /other, mention", "").strip()
                
                if title:
                    papers.append({
                        "title": title,
                        "authors": authors,
                        "department": dept,
                        "journal": journal,
                        "year": year,
                        "issn": issn,
                        "url": url,
                        "indexing": indexing
                    })
                    cursor.execute("""
                    INSERT INTO research_papers (title, authors, department, journal, year, issn, url, indexing)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (title, authors, dept, journal, year, issn, url, indexing))
                    
                    # Add to FTS table
                    cursor.execute("""
                    INSERT INTO fts_knowledge (entity_type, title, subtitle, content, source_url)
                    VALUES (?, ?, ?, ?, ?)
                    """, (
                        "research_paper",
                        title,
                        f"{authors} ({dept})",
                        f"Journal: {journal} ({year}). ISSN: {issn}. Indexing: {indexing}",
                        url or "https://kalingauniversity.ac.in/research"
                    ))
                    
    target_summary = os.path.join(KB_TARGET_DIR, "research_papers_summary.json")
    with open(target_summary, "w", encoding="utf-8") as f:
        json.dump({
            "total_papers": len(papers),
            "recent_highlights": papers[:100],
            "faculties": sorted(list(set(p["department"] for p in papers if p["department"]))),
            "years": sorted(list(set(p["year"] for p in papers if p["year"])), reverse=True)
        }, f, indent=2)
    conn.commit()
    print(f"[OK] Ingested {len(papers)} research papers -> SQLite & {target_summary}")
    return papers

def ingest_books_chapters(conn: sqlite3.Connection):
    csv_path = os.path.join(KB_SOURCE_DIR, "KU — Books and chapters (3,141).csv")
    books = []
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books_chapters;")
    
    if os.path.exists(csv_path):
        with open(csv_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                author = row.get("Name of the teacher", "").strip()
                dept = row.get("Department", "").strip()
                title = clean_html(row.get("Title of the book/chapters published", "").strip() or row.get("Title of the paper", "").strip())
                conf = row.get("Name of the conference", "").strip()
                proc = row.get("Title of the proceedings of the conference", "").strip()
                nat_intl = row.get("National / International", "").strip()
                year = row.get("Year of publication", "").strip()
                isbn = row.get("ISBN/ISSN number of the proceeding", "").strip()
                inst = row.get("Affiliating Institute at the time of publication", "").strip()
                pub = row.get("Name of the publisher", "").strip()
                
                if title or author:
                    books.append({
                        "author": author,
                        "department": dept,
                        "title": title or "Research Publication",
                        "conference": conf,
                        "proceeding_title": proc,
                        "nat_intl": nat_intl,
                        "year": year,
                        "isbn": isbn,
                        "institute": inst,
                        "publisher": pub
                    })
                    cursor.execute("""
                    INSERT INTO books_chapters (author, department, title, conference, proceeding_title, nat_intl, year, isbn, institute, publisher)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (author, dept, title, conf, proc, nat_intl, year, isbn, inst, pub))
                    
                    cursor.execute("""
                    INSERT INTO fts_knowledge (entity_type, title, subtitle, content, source_url)
                    VALUES (?, ?, ?, ?, ?)
                    """, (
                        "book_chapter",
                        title or f"Publication by {author}",
                        f"Author: {author} • {dept}",
                        f"Publisher: {pub}. ISBN: {isbn}. Year: {year}. Level: {nat_intl}. {conf}",
                        "https://kalingauniversity.ac.in/research"
                    ))
                    
    target_summary = os.path.join(KB_TARGET_DIR, "books_chapters_summary.json")
    with open(target_summary, "w", encoding="utf-8") as f:
        json.dump({
            "total_books_chapters": len(books),
            "recent_highlights": books[:100],
            "publishers": sorted(list(set(b["publisher"] for b in books if b["publisher"])))[:50]
        }, f, indent=2)
    conn.commit()
    print(f"[OK] Ingested {len(books)} books & chapters -> SQLite & {target_summary}")
    return books

def ingest_news_and_events(conn: sqlite3.Connection):
    csv_path = os.path.join(KB_SOURCE_DIR, "KU — News and events (30).csv")
    events = []
    cursor = conn.cursor()
    cursor.execute("DELETE FROM news_events;")
    
    if os.path.exists(csv_path):
        with open(csv_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                d = row.get("date", "").strip()
                heading = clean_html(row.get("heading", "").strip())
                cat = row.get("category", "").strip()
                dept = row.get("department", "").strip()
                url = row.get("url", "").strip()
                summary = clean_html(row.get("summary", "").strip())
                read_time = row.get("reading_time", "").strip()
                
                if heading:
                    events.append({
                        "date": d,
                        "heading": heading,
                        "category": cat,
                        "department": dept,
                        "url": url,
                        "summary": summary,
                        "reading_time": read_time
                    })
                    cursor.execute("""
                    INSERT INTO news_events (date, heading, category, department, url, summary, reading_time)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (d, heading, cat, dept, url, summary, read_time))
                    
                    cursor.execute("""
                    INSERT INTO fts_knowledge (entity_type, title, subtitle, content, source_url)
                    VALUES (?, ?, ?, ?, ?)
                    """, (
                        "news_event",
                        heading,
                        f"{cat} • {d}" + (f" ({dept})" if dept else ""),
                        summary,
                        url or "https://kalingauniversity.ac.in/news-and-events"
                    ))
                    
    target_path = os.path.join(KB_TARGET_DIR, "news_events.json")
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump({"total": len(events), "events": events}, f, indent=2)
    conn.commit()
    print(f"[OK] Ingested {len(events)} news and events -> SQLite & {target_path}")
    return events

def ingest_page_index(conn: sqlite3.Connection):
    csv_path = os.path.join(KB_SOURCE_DIR, "KU — Page index (199).csv")
    pages = []
    cursor = conn.cursor()
    cursor.execute("DELETE FROM page_index;")
    
    if os.path.exists(csv_path):
        with open(csv_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                slug = row.get("slug", "").strip()
                url = row.get("url", "").strip()
                title = clean_html(row.get("title", "").strip())
                desc = clean_html(row.get("meta_description", "").strip())
                chars = int(row.get("content_chars", 0) or 0)
                
                if slug or url:
                    pages.append({
                        "slug": slug,
                        "url": url,
                        "title": title,
                        "meta_description": desc,
                        "content_chars": chars
                    })
                    cursor.execute("""
                    INSERT INTO page_index (slug, url, title, meta_description, content_chars)
                    VALUES (?, ?, ?, ?, ?)
                    """, (slug, url, title, desc, chars))
                    
                    cursor.execute("""
                    INSERT INTO fts_knowledge (entity_type, title, subtitle, content, source_url)
                    VALUES (?, ?, ?, ?, ?)
                    """, (
                        "page",
                        slug.replace("-", " ").title(),
                        title,
                        f"Page: {slug}. {desc}",
                        url
                    ))
                    
    target_path = os.path.join(KB_TARGET_DIR, "page_index.json")
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump({"total": len(pages), "pages": pages}, f, indent=2)
    conn.commit()
    print(f"[OK] Ingested {len(pages)} web pages -> SQLite & {target_path}")
    return pages

def ingest_data_tables_catalogue(conn: sqlite3.Connection):
    csv_path = os.path.join(KB_SOURCE_DIR, "KU — Data table catalogue (94).csv")
    tables = []
    cursor = conn.cursor()
    cursor.execute("DELETE FROM data_tables_catalogue;")
    
    if os.path.exists(csv_path):
        with open(csv_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                tid = row.get("id", "").strip()
                title = row.get("title", "").strip()
                cat = row.get("category", "").strip()
                dept = row.get("department", "").strip()
                rows_count = int(row.get("rows", 0) or 0)
                cols_count = int(row.get("columns", 0) or 0)
                headers = row.get("headers", "").strip()
                updated = row.get("updated_at", "").strip()
                
                if title:
                    tables.append({
                        "id": tid,
                        "title": title,
                        "category": cat,
                        "department": dept,
                        "rows": rows_count,
                        "columns": cols_count,
                        "headers": headers,
                        "updated_at": updated
                    })
                    cursor.execute("""
                    INSERT INTO data_tables_catalogue (table_id, title, category, department, rows_count, columns_count, headers, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (tid, title, cat, dept, rows_count, cols_count, headers, updated))
                    
    target_path = os.path.join(KB_TARGET_DIR, "data_tables_catalogue.json")
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump({"total": len(tables), "tables": tables}, f, indent=2)
    conn.commit()
    print(f"[OK] Ingested {len(tables)} data table catalogues -> SQLite & {target_path}")
    return tables

def ingest_programmes_by_faculty(conn: sqlite3.Connection):
    csv_path = os.path.join(KB_SOURCE_DIR, "KU — Programmes by faculty (67).csv")
    progs = []
    cursor = conn.cursor()
    cursor.execute("DELETE FROM programmes_faculty;")
    
    if os.path.exists(csv_path):
        with open(csv_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                dept = row.get("department", "").strip()
                prog = row.get("programme", "").strip()
                desc = clean_html(row.get("description", "").strip())
                if dept and prog:
                    progs.append({"department": dept, "programme": prog, "description": desc})
                    cursor.execute("INSERT INTO programmes_faculty (department, programme, description) VALUES (?, ?, ?)", (dept, prog, desc))
                    
    target_path = os.path.join(KB_TARGET_DIR, "programmes_faculty.json")
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump({"total": len(progs), "programmes": progs}, f, indent=2)
    conn.commit()
    print(f"[OK] Ingested {len(progs)} faculty programmes -> SQLite & {target_path}")
    return progs

def ingest_departments_detailed(conn: sqlite3.Connection):
    json_path = os.path.join(KB_SOURCE_DIR, "KU — Structured knowledge base (JSON).json")
    dept_data = []
    cursor = conn.cursor()
    cursor.execute("DELETE FROM departments;")
    
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            full_kb = json.load(f)
            dept_data = full_kb.get("departments", [])
            for d in dept_data:
                name = d.get("name", "").strip()
                slug = d.get("slug", "").strip()
                desc = d.get("description", "").strip()
                pcount = len(d.get("programs", []))
                cursor.execute("INSERT INTO departments (name, slug, description, programs_count) VALUES (?, ?, ?, ?)", (name, slug, desc, pcount))
                
    target_path = os.path.join(KB_TARGET_DIR, "departments_detailed.json")
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump({"total": len(dept_data), "departments": dept_data}, f, indent=2)
    conn.commit()
    print(f"[OK] Ingested {len(dept_data)} departments -> SQLite & {target_path}")
    return dept_data

def update_core_kb_files(courses):
    fees_records = []
    for c in courses:
        fees_records.append({
            "program": c["program"],
            "short_name": c.get("short_name", ""),
            "level": c.get("level", ""),
            "department": c.get("department", ""),
            "duration": f"{c['tenure_years']} Years ({c['semesters']} Semesters)" if c['tenure_years'] else "N/A",
            "tuition_fee_per_sem": f"₹{c['tuition_per_semester_inr']}" if c['tuition_per_semester_inr'] else "Refer official portal",
            "exam_fee_per_sem": f"₹{c['exam_fee_per_semester_inr']}" if c['exam_fee_per_semester_inr'] else "Included",
            "one_time_fees": f"Exam Fee ₹{c['exam_fee_per_semester_inr']}/sem" if c['exam_fee_per_semester_inr'] else "Included",
            "published_total": f"₹{c['total_fees_inr']}" if c['total_fees_inr'] else "Contact Admission Office",
            "official_source": c["url"] or "https://kalingauniversity.ac.in/ku-fees"
        })
    
    fees_json = {
        "note": "Fee details extracted directly from official Kalinga University 2026-27 published course schedules.",
        "fee_records": fees_records,
        "additional_information": {
            "caution_money": "₹5,000 (One-time, refundable)",
            "kalsee_fee": "₹1,000 (₹1,200 for NRI / Foreign Students)",
            "hostel_fee": "7-Occupancy: ₹60,000/yr, 4-Occupancy: ₹76,000/yr, 3-Occupancy: ₹92,000/yr (Air-Cooled), AC options available"
        }
    }
    with open(os.path.join(KB_TARGET_DIR, "fees.json"), "w", encoding="utf-8") as f:
        json.dump(fees_json, f, indent=2)
    print(f"[OK] Enriched fees.json with {len(fees_records)} course fee records")

def print_database_summary(conn: sqlite3.Connection):
    cursor = conn.cursor()
    tables = [
        "courses", "course_faqs", "career_paths", "training_internships",
        "mous_collaborations", "patents", "research_papers", "books_chapters",
        "news_events", "page_index", "data_tables_catalogue", "programmes_faculty", "departments"
    ]
    print("\n" + "="*60)
    print("KALINGA UNIVERSITY SQLITE DATABASE INGESTION SUMMARY")
    print("="*60)
    total_records = 0
    for t in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {t}")
        cnt = cursor.fetchone()[0]
        total_records += cnt
        print(f"• {t.ljust(25)} : {cnt:>6} records")
    
    cursor.execute("SELECT COUNT(*) FROM fts_knowledge")
    fts_cnt = cursor.fetchone()[0]
    print(f"• {'fts_knowledge (FTS5 index)'.ljust(25)} : {fts_cnt:>6} indexed search documents")
    print("-"*60)
    print(f"TOTAL GROUNDED UNIVERSITY RECORDS : {total_records:>6}")
    print("="*60 + "\n")

def main():
    os.makedirs(KB_TARGET_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    setup_sqlite_tables(conn)
    
    courses = ingest_courses_detailed(conn)
    ingest_course_faqs(conn)
    ingest_career_paths(conn)
    ingest_internships_detailed(conn)
    ingest_mous_collaborations(conn)
    ingest_research_patents(conn)
    ingest_research_papers(conn)
    ingest_books_chapters(conn)
    ingest_news_and_events(conn)
    ingest_page_index(conn)
    ingest_data_tables_catalogue(conn)
    ingest_programmes_by_faculty(conn)
    ingest_departments_detailed(conn)
    update_core_kb_files(courses)
    
    print_database_summary(conn)
    conn.close()

if __name__ == "__main__":
    main()
