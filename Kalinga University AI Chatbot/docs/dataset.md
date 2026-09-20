# Dataset Documentation — Kalinga University AI Chatbot

## Provenance
The dataset for this project was derived directly from the official Kalinga University source document (`Kalinga_University_Admission_Fees_Courses_Internships_Placements_Analysis_2026-27.docx`) and verified against official university web pages.

## Directory Structure
- `data/raw/`: Original source document.
- `data/knowledge_base/`:
  - `university.json`: Location, overview, claims (130+ programs, 650+ international students, 400+ recruiters, 7,200+ publications, 562+ patents).
  - `admissions.json`: Step-by-step admission procedure, required documents, KALSEE & KAL-MAT exam details.
  - `courses.json`: Selected course list grouped across 10 faculties.
  - `fees.json`: Visible 2026-27 fee table for Arts & Humanities programs and fallback rules.
  - `scholarships.json`: Scholarship categories (up to 100%) and claims.
  - `internships.json`: On-campus/off-campus internships, 6-month CoE initiative, and published student highlights.
  - `placements.json`: Published individual high package highlights (₹33 LPA LLM, ₹29.98 LPA B.Tech), 28 top recruiters list, and historical brochure stats.
  - `campus.json`: Campus amenities, 100+ labs, 7 CoE labs, sports complex, and hostels.
- `data/processed/`:
  - `intents.json`: 33 intent classes with natural language patterns and responses.
  - `faq_dataset.json`: 248 pattern-response training pairs.
  - `faq_dataset.csv`: Tabular CSV version of the FAQ dataset.
