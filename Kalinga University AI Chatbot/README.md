# Kalinga University AI Student Query Chatbot
> **College Minor Project**: NLP-Based Intelligent Student Support Chatbot for Kalinga University (Raipur, Chhattisgarh).

---

## Key Features
- **Explainable NLP Pipeline**: Powered by TF-IDF vectorization and scikit-learn Logistic Regression intent classification (33 intent categories).
- **Zero-Hallucination Policy**: Grounded strictly in official university source material (`Kalinga_University_Admission_Fees_Courses_Internships_Placements_Analysis_2026-27.docx`). Unlisted data directs students to official portals rather than inventing fake fees or numbers.
- **Source Attribution**: Every factual answer includes clickable official Kalinga University URL verification links.
- **Multi-Turn Session Context**: Remembers previous query intent and program context across sequential questions (e.g. *"What is the fee for BBA?"* -> *"What about MBA?"*).
- **Interactive Knowledge Base Explorer**: Built-in modal for students to explore 11,070+ records including 2026-27 fee tables, recruiter lists, scholarship options, and academic faculties.
- **Progressive Web App (PWA)**: 1-Click installable on Windows, macOS, Android, and iOS with offline shell caching via Service Worker.
- **Multi-Device Local Access**: Built-in QR code sharing for opening and installing the chatbot on phones and tablets across any local Wi-Fi / LAN network.
- **Modern Student UI**: Built with React 18, Vite, TypeScript, and Tailwind CSS featuring a Neumorphic aesthetic, typing indicators, suggested questions, and responsive layout.

---

> 📖 **Comprehensive Guides & Documentation**:
> - **[Development, Dataset & Deployment Guide](docs/DEVELOPMENT_AND_DEPLOYMENT_GUIDE.md)**: Full step-by-step setup, dataset schema, retraining pipeline, production deployment (Docker, PaaS, Linux VPS), and official reference links.
> - **[Project Minor Report](docs/project-report.md)**: Academic project report.
> - **[System Architecture](docs/architecture.md)**: Sequence and flowchart diagrams.
> - **[Dataset Documentation](docs/dataset.md)**: Data provenance and file formats.
> - **[Testing Documentation](docs/testing.md)**: Pytest execution logs and test cases.

---

## Tech Stack
- **Frontend**: React 18, Vite 5, TypeScript, Tailwind CSS 3, Lucide React
- **Backend**: Python 3.13, FastAPI, Uvicorn, Pydantic v2
- **NLP / ML**: scikit-learn, pandas, numpy, python-docx, joblib
- **Testing**: Pytest, HTTPX

---

## Quick Start & Running Commands

### 1. Prerequisites
- Python 3.10+
- Node.js v18+ & npm

### 2. Backend Setup & Run

```bash
# Navigate to backend directory
cd backend

# Create & activate virtual environment (Windows)
python -m venv .venv
.venv\Scripts\activate

# Install backend dependencies
pip install -r requirements.txt

# Run FastAPI backend server (Port 8000)
uvicorn app.main:app --reload --port 8000
```

The backend server will run at `http://localhost:8000`. Swagger API docs are accessible at `http://localhost:8000/docs`.

### 3. Frontend Setup & Run

```bash
# Navigate to frontend directory
cd frontend

# Install NPM dependencies
npm install

# Run Vite dev server (Port 5173)
npm run dev
```

The frontend chat UI will be accessible at `http://localhost:5173`.

---

## Model Training & Evaluation

To re-extract source data, generate dataset JSONs, retrain the NLP model, and run evaluation benchmark queries:

```bash
# Extract source docx & build knowledge base
python scripts/extract_source_data.py

# Build dataset JSON & CSV files
python scripts/build_dataset.py

# Train NLP model & save artifacts to backend/models/
backend\.venv\Scripts\python scripts/train_model.py

# Run benchmark evaluation queries
backend\.venv\Scripts\python scripts/evaluate_model.py
```

---

## Automated Pytest Suite

To run the complete automated Pytest test suite covering API endpoints, NLP classification, safety fallbacks, and multi-turn context:

```bash
backend\.venv\Scripts\pytest backend/tests/
```

**Results**: `15 passed out of 15 tests (100% PASS)`

---

## Project Structure

```
d:\Kalinga University AI Chatbot\
├── README.md
├── AGENTS.md
├── .env.example
├── .gitignore
├── .agents/                      # Rules and skills
├── data/                         # Raw, processed & knowledge base JSON files
│   ├── raw/
│   ├── processed/
│   ├── knowledge_base/
│   └── source_registry.json
├── scripts/                      # Data extraction, training & evaluation scripts
├── backend/                      # FastAPI server, models, services & tests
│   ├── app/
│   ├── models/
│   ├── tests/
│   └── requirements.txt
├── frontend/                     # React Vite TypeScript Tailwind UI
│   ├── src/
│   └── package.json
└── docs/                         # Minor project report & architecture docs
    ├── DEVELOPMENT_AND_DEPLOYMENT_GUIDE.md
    ├── project-report.md
    ├── architecture.md
    ├── dataset.md
    └── testing.md
```
