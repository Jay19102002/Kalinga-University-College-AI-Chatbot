# College Minor Project Report
## AI Chatbot for Student Queries — Kalinga University
*Alternative Title: NLP-Based Intelligent Student Support Chatbot for Kalinga University*

---

### Abstract
In higher education institutions, students and prospective applicants frequently inquire about admissions, eligibility criteria, fee structures, entrance examinations (KALSEE/KAL-MAT), scholarships, internship opportunities, and campus placements. Manual handling of repetitive queries strains administrative staff and leads to delayed responses. This project presents an explainable, lightweight Natural Language Processing (NLP) student assistant chatbot designed specifically for Kalinga University, Raipur. Built using React, Vite, TypeScript, and Tailwind CSS on the frontend and FastAPI, scikit-learn (TF-IDF + Logistic Regression), and Pydantic on the backend, the chatbot understands natural language queries, classifies intent, extracts key entities, maintains multi-turn session context, and retrieves source-grounded answers. Crucially, the system enforces zero hallucination by qualifying university claims and providing clickable attribution links to official Kalinga University web pages.

---

### 1. Introduction
Modern university web portals contain extensive information distributed across numerous subpages. Finding specific information regarding fee breakups, application procedures, or entrance exam formats can be overwhelming for prospective students. This project develops an intelligent automated chatbot that provides instant, reliable answers to student queries while operating completely offline without paid cloud LLM dependencies.

---

### 2. Problem Statement
1. **Navigational Complexity**: Students often struggle to locate exact program-specific fee structures or eligibility guidelines on university websites.
2. **Hallucination & Misinformation in Generic AI**: General-purpose AI models frequently hallucinate fake fee amounts or promise guaranteed placements.
3. **High Operational Costs**: Commercial LLM APIs require continuous usage fees and internet availability, making them impractical for standard college minor projects.

---

### 3. Proposed Solution & Objectives
The proposed system addresses these challenges through:
- **Source-Grounded Knowledge Base**: Derived strictly from Kalinga University's official source material.
- **Explainable Lightweight NLP Pipeline**: Utilizing TF-IDF vectorization and Logistic Regression for transparent intent classification.
- **Zero Hallucination Guarantee**: Unlisted fees or statistics return an explicit, helpful fallback directing students to official portals rather than inventing data.
- **Multi-Turn Context Tracking**: Retaining previous query intent and entity focus (e.g. tracking program name across sequential questions).
- **Source Attribution**: Attaching clickable official university URL links to every answer.

---

### 4. System Architecture
The application follows a decoupled client-server architecture:
1. **Frontend**: React + Vite + TypeScript + Tailwind CSS delivering a modern responsive student chat interface with suggested query pills, typing indicators, entity badges, and an interactive Knowledge Base modal.
2. **Backend Server**: FastAPI REST API server providing `/api/health`, `/api/chat`, and structured knowledge retrieval endpoints (`/api/courses`, `/api/fees`, `/api/scholarships`, etc.).
3. **NLP Engine**: Preprocessing normalizer, TF-IDF feature extractor (1-2 ngrams), Logistic Regression classifier, rule-based entity extractor, and session context manager.

---

### 5. Technologies Used
- **Frontend**: React 18, Vite 5, TypeScript, Tailwind CSS 3, Lucide React icons.
- **Backend**: Python 3.13, FastAPI, Uvicorn, Pydantic v2.
- **NLP & Data Handling**: scikit-learn, pandas, numpy, python-docx, joblib.
- **Testing**: Pytest, HTTPX, requests.

---

### 6. NLP Methodology
1. **Text Preprocessing**: Lowercasing, acronym standardization (e.g. `B.Tech` -> `btech`, `KALSEE` -> `kalsee`), punctuation cleaning, and whitespace collapsing.
2. **Vectorization**: TF-IDF (Term Frequency-Inverse Document Frequency) using unigrams and bigrams (`ngram_range=(1,2)`).
3. **Intent Classification**: Supervised Logistic Regression classifier predicting probability distributions across 33 distinct intent categories.
4. **Entity Extraction**: Regex pattern matcher identifying program names (BBA, MBA, B.Tech, MCA, LLB, B.Pharm), entrance exams (KALSEE, KAL-MAT), and query types.
5. **Context Management**: Tracking `last_intent` and `last_program` per `session_id` to interpret follow-up queries like *"What about MBA?"*.

---

### 7. Experimental Results & Testing
- **Training Accuracy**: 100.00% across 248 training patterns.
- **Macro F1 Score**: 100.00%.
- **Benchmark Evaluation Accuracy**: 93.33% (14 out of 15 sample benchmark queries correctly classified).
- **Pytest Suite**: 15 out of 15 automated unit tests passed (100% PASS).

---

### 8. Limitations & Future Scope
- **Current Limitations**: The static knowledge base reflects visible source records for 2026-27; dynamically loaded fee tables for non-Arts faculties direct students to official web links.
- **Future Scope**:
  - Integration of multilingual support (Hindi and regional languages).
  - Voice query input and text-to-speech output.
  - Integration with university student portal APIs for live fee payment status checks.

---

### 9. Conclusion
The Kalinga University AI Student Query Chatbot successfully demonstrates an explainable, reliable, and source-grounded NLP solution for answering student inquiries. By combining lightweight machine learning with strict data integrity, the system provides an impressive, production-quality project suitable for a college minor-project demonstration.

---

### References
1. Kalinga University Official Web Portal: https://kalingauniversity.ac.in/
2. Kalinga University Admission Procedure: https://kalingauniversity.ac.in/admission-procedure
3. Scikit-learn: Machine Learning in Python, Pedregosa et al., JMLR 12, pp. 2825-2830, 2011.
4. FastAPI Documentation: https://fastapi.tiangolo.com/
