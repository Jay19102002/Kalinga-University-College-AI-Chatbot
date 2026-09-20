import os
import json
# pyrefly: ignore [missing-import]
import joblib
from typing import Dict, Any, List, Tuple, Optional
from app.config import settings
from app.nlp.preprocessing import normalize_text
from app.nlp.entity_extractor import extract_entities
from app.services.retrieval import kb_service
from app.services.database import db_service
from app.schemas import SourceItem

class SessionContext:
    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}

    def get_context(self, session_id: str) -> Dict[str, Any]:
        return self.sessions.get(session_id, {})

    def update_context(self, session_id: str, intent: str, entities: Dict[str, Any]):
        if session_id not in self.sessions:
            self.sessions[session_id] = {}
        
        ctx = self.sessions[session_id]
        ctx["last_intent"] = intent
        if "program" in entities:
            ctx["last_program"] = entities["program"]
        if "entrance_exam" in entities:
            ctx["last_entrance_exam"] = entities["entrance_exam"]

session_context = SessionContext()

class ChatbotService:
    def __init__(self):
        self.vectorizer = None
        self.classifier = None
        self.label_encoder = None
        self.intents_data: Dict[str, Any] = {}
        self._load_model()
        self._load_intents()

    def _load_model(self):
        v_path = os.path.join(settings.MODEL_DIR, "tfidf_vectorizer.joblib")
        c_path = os.path.join(settings.MODEL_DIR, "intent_classifier.joblib")
        l_path = os.path.join(settings.MODEL_DIR, "label_encoder.joblib")
        
        if os.path.exists(v_path) and os.path.exists(c_path) and os.path.exists(l_path):
            self.vectorizer = joblib.load(v_path)
            self.classifier = joblib.load(c_path)
            self.label_encoder = joblib.load(l_path)
            print("Loaded trained NLP model artifacts.")
        else:
            print("Warning: NLP model artifacts not found. Please run scripts/train_model.py.")

    def _load_intents(self):
        intents_file = os.path.join(settings.DATA_DIR, "processed", "intents.json")
        if os.path.exists(intents_file):
            with open(intents_file, "r", encoding="utf-8") as f:
                self.intents_data = json.load(f)

    def process_query(self, user_message: str, session_id: Optional[str] = "default_session") -> Tuple[str, str, float, Dict[str, Any], List[SourceItem]]:
        if not user_message or not user_message.strip():
            return (
                "Please enter a question so I can help you with Kalinga University information.",
                "empty_input",
                1.0,
                {},
                [SourceItem(title="Kalinga University Homepage", url="https://kalingauniversity.ac.in/")]
            )

        if len(user_message) > settings.MAX_MESSAGE_LENGTH:
            return (
                f"Your query exceeds the maximum allowed length of {settings.MAX_MESSAGE_LENGTH} characters. Please ask a shorter question.",
                "long_input",
                1.0,
                {},
                []
            )

        # 1. Preprocessing & Entity Extraction
        clean_text = normalize_text(user_message)
        entities = extract_entities(user_message)
        ctx = session_context.get_context(session_id)

        # 2. Domain-Specific Topic Overrides (Research, Books, News, Patents)
        intent_override = None
        lower_msg = user_message.lower()

        if any(w in lower_msg for w in ["research paper", "research papers", "scopus", "ugc care", "faculty publication"]):
            intent_override = "research_papers"
        elif any(w in lower_msg for w in ["book", "books published", "chapters published", "conference proceeding"]):
            intent_override = "books_chapters"
        elif any(w in lower_msg for w in ["patent", "patents", "invention", "granted patent"]):
            intent_override = "patents"
        elif any(w in lower_msg for w in ["ideathon", "upcoming event", "news and events", "workshop", "toppers felicitation"]):
            intent_override = "news_events"
        elif "program" in entities and ("fee" in clean_text or ctx.get("last_intent") in ["fees", "course_fee", "semester_fee"]):
            if any(term in clean_text for term in ["what about", "how about", "cost for", "fee for", "and mba", "and bba"]):
                intent_override = "course_fee"

        # 3. Intent Classification
        if self.vectorizer and self.classifier and self.label_encoder and not intent_override:
            vec = self.vectorizer.transform([clean_text])
            pred_idx = self.classifier.predict(vec)[0]
            probs = self.classifier.predict_proba(vec)[0]
            confidence = float(probs[pred_idx])
            pred_intent = self.label_encoder.inverse_transform([pred_idx])[0]
        elif intent_override:
            pred_intent = intent_override
            confidence = 0.95
        else:
            pred_intent = "unknown"
            confidence = 0.0

        # 4. Context & Entity enrichment
        if "program" not in entities:
            for phrase in ["fee for", "fees for", "cost of", "fee of", "fee structure for"]:
                if phrase in lower_msg:
                    cand = lower_msg.split(phrase)[-1].replace("?", "").strip()
                    if cand:
                        entities["program"] = cand
                        break

        if "program" not in entities and ctx.get("last_program") and pred_intent in ["course_fee", "bba_courses", "mba_courses", "btech_courses", "internship", "placement"]:
            entities["program"] = ctx["last_program"]

        # Update context
        # pyrefly: ignore [bad-argument-type]
        session_context.update_context(session_id, pred_intent, entities)

        # 5. Fallback & Full-Text Search Check
        if confidence < settings.CONFIDENCE_THRESHOLD and not intent_override and not entities.get("program"):
            # Check FTS5 database before falling back
            fts_matches = db_service.search_global(clean_text, limit=3)
            if fts_matches:
                top = fts_matches[0]
                ans = f"Based on the Kalinga University Knowledge Base for '{top['title']}':\n\n" \
                      f"• {top['subtitle']}\n" \
                      f"• {top['content']}"
                sources = [SourceItem(title=top['title'], url=top['source_url'])]
                return ans, "fts_retrieval", 0.75, entities, sources
            
            return (
                "I'm not fully sure about that question. I can currently help with:\n"
                "• Admissions & Entrance Exams (KALSEE / KAL-MAT)\n"
                "• Courses & 2026-27 Fees (69 programs)\n"
                "• Scholarships (up to 100%)\n"
                "• Research Publications (4,869 Scopus papers)\n"
                "• Books & Chapters (3,141 published by faculty)\n"
                "• Patents & Innovations (600 patents)\n"
                "• Internships & Corporate Trainings (649 records)\n"
                "• MoUs & Collaborations (438 partners)\n"
                "• Upcoming News & Events (Ideathon 6.0, Workshops)\n\n"
                "Please rephrase your question or explore the Knowledge Base Portal.",
                "unknown",
                confidence,
                entities,
                [SourceItem(title="Kalinga University Homepage", url="https://kalingauniversity.ac.in/")]
            )

        # 6. Response Generation & Retrieval
        answer, sources = self._generate_response(pred_intent, entities, clean_text, user_message)
        return answer, pred_intent, confidence, entities, sources

    def _generate_response(self, intent: str, entities: Dict[str, Any], clean_text: str, user_message: str = "") -> Tuple[str, List[SourceItem]]:
        # Fee queries with specific program
        if intent in ["course_fee", "fees", "semester_fee"]:
            program = entities.get("program")
            if not program and user_message:
                for phrase in ["fee for", "fees for", "cost of", "fee of", "fee structure for"]:
                    if phrase in user_message.lower():
                        cand = user_message.lower().split(phrase)[-1].replace("?", "").strip()
                        if cand:
                            program = cand
                            break

            if program:
                fee_res = kb_service.get_fee_info(program)
                if fee_res.get("found") and "record" in fee_res:
                    rec = fee_res["record"]
                    ans = f"According to Kalinga University's published 2026-27 fee structure for {rec['program']} ({rec.get('department', 'Faculty')}):\n" \
                          f"• Duration: {rec['duration']}\n" \
                          f"• Tuition Fee: {rec['tuition_fee_per_sem']} per semester\n" \
                          f"• Examination Fee: {rec.get('exam_fee_per_sem', '₹1,500/sem')}\n" \
                          f"• One-time Fees: {rec['one_time_fees']}\n" \
                          f"• Total Published Program Fee: {rec['published_total']}"
                    sources = [SourceItem(title=s["title"], url=s["url"]) for s in fee_res["sources"]]
                    return ans, sources
                else:
                    ans = f"I don't have a reliable fee value for '{program}' in my current knowledge base. Please check Kalinga University's official fee page at https://kalingauniversity.ac.in/ku-fees."
                    sources = [SourceItem(title="Kalinga University Official Fee Page", url="https://kalingauniversity.ac.in/ku-fees")]
                    return ans, sources

        # Research Papers query
        if intent == "research_papers":
            papers_data = db_service.get_research_papers(query=clean_text if "paper" not in clean_text else None, limit=3)
            papers = papers_data.get("papers", [])
            total = papers_data.get("total", 4866)
            ans = f"Kalinga University has a strong research track record with over {total} published research papers listed in Scopus and UGC Care.\n\nRecent Publications:"
            for p in papers:
                ans += f"\n• \"{p['title']}\" by {p['authors']} ({p['department']}) — {p['journal']} ({p['year']})"
            ans += "\n\nYou can explore all 4,869 research papers with Scopus links in the Knowledge Base Portal."
            sources = [SourceItem(title="Kalinga University Research & Scopus Publications", url="https://kalingauniversity.ac.in/research")]
            return ans, sources

        # Books and Chapters query
        if intent == "books_chapters":
            books_data = db_service.get_books_chapters(query=clean_text if "book" not in clean_text else None, limit=3)
            books = books_data.get("books", [])
            total = books_data.get("total", 3141)
            ans = f"Kalinga University faculty have authored and published over {total} books and book chapters across national and international publishers.\n\nFeatured Publications:"
            for b in books:
                ans += f"\n• \"{b['title']}\" by {b['author']} ({b['department']}) — Publisher: {b['publisher']} ({b['year']})"
            ans += "\n\nYou can browse all 3,141 book chapters in the Knowledge Base Portal."
            sources = [SourceItem(title="Kalinga University Faculty Books & Publications", url="https://kalingauniversity.ac.in/research")]
            return ans, sources

        # Patents query
        if intent == "patents":
            patents = db_service.get_patents(limit=3)
            ans = f"Kalinga University holds over 600 innovation patents filed and granted across engineering, pharmacy, science, and computing.\n\nRecent Highlights:"
            for p in patents:
                ans += f"\n• {p['topic']} (Inventor: {p['inventor']}, Status: {p['status']}, App No: {p['app_no']})"
            ans += "\n\nAll 600 patents can be searched in the Knowledge Base Portal."
            sources = [SourceItem(title="Kalinga University Patents & Innovations", url="https://kalingauniversity.ac.in/research")]
            return ans, sources

        # News & Events query
        if intent == "news_events":
            events = db_service.get_news_events(limit=3)
            ans = "Here are key news and events from Kalinga University:\n"
            for ev in events:
                ans += f"\n• {ev['heading']} ({ev['date']}) — {ev['category']}\n  {ev['summary']}"
            sources = [SourceItem(title="Kalinga University News & Events", url="https://kalingauniversity.ac.in/news-and-events")]
            return ans, sources

        # Default response lookup from dataset intents
        for item in self.intents_data.get("intents", []):
            if item["intent"] == intent:
                ans = item["responses"][0]
                if entities.get("program") and intent in ["bba_courses", "mba_courses", "btech_courses", "bca_courses", "mca_courses", "law_courses", "pharmacy_courses"]:
                    ans += f"\n(Note: Program details apply to {entities['program']}.)"
                
                urls = item.get("source_urls", ["https://kalingauniversity.ac.in/"])
                sources = [SourceItem(title=f"Kalinga University — {intent.replace('_', ' ').title()}", url=u) for u in urls]
                return ans, sources

        # Fallback
        return (
            "I'm not fully sure about that question. Please rephrase your question or visit the official Kalinga University portal.",
            [SourceItem(title="Kalinga University Homepage", url="https://kalingauniversity.ac.in/")]
        )

chatbot_service = ChatbotService()
