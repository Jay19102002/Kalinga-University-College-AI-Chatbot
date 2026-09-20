# Kalinga University AI Chatbot — Development, Dataset & Deployment Guide

> **Official College Minor Project Guide**  
> Complete documentation covering development setup, dataset provenance & schema, NLP pipeline retraining, multi-device PWA deployment, and production hosting options for the Kalinga University AI Student Support Chatbot.

---

## Table of Contents
1. [Project Overview & System Architecture](#1-project-overview--system-architecture)
2. [Step-by-Step Development Setup](#2-step-by-step-development-setup)
3. [Multi-Device Access & PWA Testing](#3-multi-device-access--pwa-testing)
4. [Dataset Details & Knowledge Engine](#4-dataset-details--knowledge-engine)
5. [Model Retraining & Data Pipeline](#5-model-retraining--data-pipeline)
6. [Step-by-Step Deployment Guidance](#6-step-by-step-deployment-guidance)
   - [Option A: Docker & Docker Compose](#option-a-docker--docker-compose)
   - [Option B: Cloud PaaS (Render / Railway)](#option-b-cloud-paas-render--railway)
   - [Option C: Linux VPS (Nginx + Systemd + SSL)](#option-c-linux-vps-nginx--systemd--ssl)
   - [Option D: Campus On-Premises Showcase (Windows / LAN)](#option-d-campus-on-premises-showcase-windows--lan)
7. [Official Reference Links & Source Registry](#7-official-reference-links--source-registry)

---

## 1. Project Overview & System Architecture

The Kalinga University AI Chatbot is designed to provide real-time, zero-hallucination student guidance regarding admissions, entrance examinations (KALSEE & KAL-MAT), course syllabi, fee structures, merit scholarships, campus facilities, research publications, and career placements.

### Architectural Highlights
- **Explainable NLP Engine**: Scikit-learn TF-IDF Vectorizer with tuned sublinear term frequencies and Logistic Regression classifier across **33 intent categories**.
- **Dual-Engine Grounded Intelligence**: High-confidence student queries trigger specific verified responses; entity-driven queries dynamically consult a local SQLite database of **11,070+ records**.
- **Progressive Web App (PWA)**: Installable natively on Windows, macOS, Android, and iOS with full offline caching capabilities via Service Worker (`sw.js`).
- **LAN Multi-Device Access**: Automatic host discovery and QR code pairing allow any phone or tablet on the same Wi-Fi network to connect and install the application instantly.

```
       [ Client Devices ]
(Mobile / Tablet / PC Browser / PWA)
                │
                ▼ (HTTP / JSON / Port 5173)
     [ Vite Frontend Proxy ]
                │
                ▼ (Port 8000)
    [ FastAPI Application Server ]
          │                  │
          ▼                  ▼
[ NLP Intent Classifier ]  [ SQLite Knowledge Engine ]
(TF-IDF + Logistic Reg)    (11,070+ Grounded Records)
          │                  │
          └─────────┬────────┘
                    ▼
     [ Response Assembly Engine ]
  (Direct Answer + Verified Sources)
```

---

## 2. Step-by-Step Development Setup

### System Prerequisites
- **Python**: Version 3.10, 3.11, 3.12, or 3.13
- **Node.js**: Version 18+ (tested on Node v24 LTS)
- **Package Managers**: `pip` and `npm`

### Step 1: Clone or Navigate to Workspace
```bash
cd "d:\Kalinga University AI Chatbot"
```

### Step 2: Backend Virtual Environment Setup
Open a terminal in the root directory:
```bash
# Navigate to backend folder
cd backend

# Create Python virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# On Windows (CMD):
.\.venv\Scripts\activate.bat
# On Linux / macOS:
source .venv/bin/activate

# Upgrade pip & install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3: Frontend Dependencies Setup
Open a separate terminal window:
```bash
# Navigate to frontend folder
cd frontend

# Install Node packages
npm install
```

### Step 4: Run Both Servers (1-Click Batch Script)
For Windows users, launch both backend and frontend concurrently with dynamic IP network binding:
```cmd
run_project.bat
```
Alternatively, start them manually:
```bash
# Terminal 1: Backend Server (Port 8000)
cd backend
.\.venv\Scripts\python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Frontend Dev Server (Port 5173)
cd frontend
npm run dev -- --host 0.0.0.0
```

### Step 5: Verify Automated Test Suite
Ensure all 24 automated unit and integration tests pass:
```bash
.\backend\.venv\Scripts\pytest backend/tests -v
```

---

## 3. Multi-Device Access & PWA Testing

### Accessing the Web Application
- **Local PC**: Open `http://localhost:5173`
- **Other Devices on Wi-Fi**: Open `http://<YOUR_LOCAL_IP>:5173` (e.g., `http://10.68.177.226:5173`)
- **Backend API & Swagger Docs**: Open `http://localhost:8000/docs`

### Testing Progressive Web App (PWA) Installation
1. **Google Chrome / Microsoft Edge (Desktop)**:
   - Notice the **"Install App"** button in the header bar, or click the install icon in the browser address bar.
   - Click **Install** to add the application to your Desktop and Start menu.
2. **Android (Chrome)**:
   - Connect your phone to the same Wi-Fi network.
   - Scan the QR code from the **"Connect Devices"** modal in the header.
   - Tap **"Install App"** or tap Chrome menu (⋮) → **"Add to Home screen"**.
3. **iPhone / iPad (Safari)**:
   - Scan the QR code and open in Safari.
   - Tap the **Share** button (⎋) at the bottom.
   - Scroll down and tap **"Add to Home Screen"** (⊞).

---

## 4. Dataset Details & Knowledge Engine

### Grounded Source Provenance
The chatbot's knowledge base is synthesized from official university materials:
1. **Primary Analysis Document**: `data/raw/Kalinga_University_Admission_Fees_Courses_Internships_Placements_Analysis_2026-27.docx`
2. **Official University Portal**: Scraped and structured data from `https://kalingauniversity.ac.in/`
3. **Source Registry**: Full mapping in `data/source_registry.json`

### Dataset Breakdown

| Dataset File / Table | Record Count | Description |
| :--- | :--- | :--- |
| `data/processed/intents.json` | 33 Classes | Student intent definitions, query patterns, and response templates |
| `data/processed/faq_dataset.json` | 248 Pairs | Clean training pairs mapped across admissions, exams, fees, scholarships |
| `data/processed/faq_dataset.csv` | 248 Rows | Tabular representation for ML benchmarks and confusion matrix tests |
| `data/knowledge_base/university.json` | 1 Grounded Set | Campus specs, accreditations (NAAC, NIRF, AICTE, UGC), 562+ patents |
| `data/knowledge_base/admissions.json` | Complete Workflow | KALSEE & KAL-MAT pattern, eligibility criteria, required documents |
| `data/knowledge_base/fees.json` | Complete 2026-27 | Semester fee tables for Arts, Commerce, Tech, Pharmacy, Law, Science |
| `data/knowledge_base/scholarships.json` | 12 Categories | Merit, Defense, Siblings, Sports, Social Category criteria (up to 100%) |
| `data/knowledge_base/placements.json` | 28 Top Recruiters | Highest packages (₹33 LPA LLM, ₹29.98 LPA B.Tech), hiring partners |
| `data/kalinga_university.db` | **11,070 Records** | Unified SQLite database containing research papers, faculty books, news |

### SQLite Database Schema (`data/kalinga_university.db`)

#### Table: `knowledge_entities`
- `id` (INTEGER PRIMARY KEY)
- `entity_type` (TEXT: `program`, `faculty`, `facility`, `scholarship`, `policy`)
- `name` (TEXT: e.g., "Bachelor of Technology in Computer Science")
- `code` (TEXT: e.g., "BTECH_CSE")
- `description` (TEXT: Detailed syllabus & eligibility info)
- `metadata_json` (TEXT: Fee breakdown, duration, credits)
- `source_url` (TEXT: Official verification link)

#### Table: `research_papers`
- `id` (INTEGER PRIMARY KEY)
- `title` (TEXT)
- `authors` (TEXT)
- `department` (TEXT)
- `journal` (TEXT)
- `year` (INTEGER)
- `doi_url` (TEXT)

#### Table: `books_catalogue`
- `id` (INTEGER PRIMARY KEY)
- `title` (TEXT)
- `author` (TEXT)
- `isbn` (TEXT)
- `department` (TEXT)
- `call_number` (TEXT)

---

## 5. Model Retraining & Data Pipeline

Whenever new university circulars, fee updates, or admissions guidelines are published, re-run the pipeline in four simple steps:

```bash
# 1. Re-extract knowledge base JSONs from source DOCX
python scripts/extract_source_data.py

# 2. Build NLP training dataset (intents.json, faq_dataset.json & csv)
python scripts/build_dataset.py

# 3. Ingest records into SQLite knowledge database
python scripts/ingest_full_kb.py

# 4. Train NLP model artifacts & evaluate accuracy
backend\.venv\Scripts\python scripts/train_model.py
backend\.venv\Scripts\python scripts/evaluate_model.py
```

### Regenerating PWA Branding Icons
If the logo or branding changes, re-run the Python icon generator:
```bash
backend\.venv\Scripts\python scripts/generate_pwa_icons.py
```
This updates `pwa-192.png`, `pwa-512.png`, `maskable-icon-512.png`, `apple-touch-icon.png`, and `favicon.svg` inside `frontend/public/`.

---

## 6. Step-by-Step Deployment Guidance

### Option A: Docker & Docker Compose (Recommended for Production)

Create a `Dockerfile` in the root:
```dockerfile
# Build Stage for Frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Stage for Backend & Production Serving
FROM python:3.12-slim
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

COPY backend/ backend/
COPY data/ data/
COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist

ENV PORT=8000
EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Run with Docker Compose:
```bash
docker build -t kalinga-ai-chatbot .
docker run -d -p 8000:8000 --name kalinga-chatbot kalinga-ai-chatbot
```

---

### Option B: Cloud PaaS (Render / Railway)

#### Deploying on Render.com
1. **Backend Web Service**:
   - Environment: `Python 3`
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port $PORT`
2. **Frontend Static Site**:
   - Environment: `Node`
   - Root Directory: `frontend`
   - Build Command: `npm install && npm run build`
   - Publish Directory: `dist`
   - Add Rewrite Rule: `/api/*` → `https://<your-backend-app>.onrender.com/api/*`

---

### Option C: Linux VPS (Nginx + Systemd + SSL)

For hosting on an Ubuntu 22.04 / 24.04 VPS:

#### 1. Systemd Service (`/etc/systemd/system/kalinga-backend.service`)
```ini
[Unit]
Description=Kalinga University Chatbot FastAPI Backend
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/kalinga-chatbot/backend
ExecStart=/var/www/kalinga-chatbot/backend/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 2
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start backend:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now kalinga-backend
```

#### 2. Nginx Reverse Proxy Configuration (`/etc/nginx/sites-available/kalinga-chatbot`)
```nginx
server {
    server_name chatbot.kalingauniversity.ac.in;

    # Serve Built Frontend
    root /var/www/kalinga-chatbot/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Proxy API Requests to FastAPI Backend
    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable SSL via Let's Encrypt:
```bash
sudo certbot --nginx -d chatbot.kalingauniversity.ac.in
```

---

### Option D: Campus On-Premises Showcase (Windows / LAN)

To showcase this system during minor project viva, presentations, or campus kiosks without internet dependency:
1. Connect the host computer and test mobile devices to the same local Wi-Fi or router.
2. Double-click `run_project.bat`.
3. Read the displayed network address:
   ```text
   Phone / Other Devices: http://192.168.x.x:5173
   ```
4. Have evaluators scan the on-screen QR code to interact with and install the application directly on their phones.

---

## 7. Official Reference Links & Source Registry

### Official University Links
- **University Main Portal**: [kalingauniversity.ac.in](https://kalingauniversity.ac.in/)
- **Online Admissions 2026-27**: [kalingauniversity.ac.in/admissions](https://kalingauniversity.ac.in/admissions)
- **KALSEE Entrance Examination**: [kalingauniversity.ac.in/kalsee](https://kalingauniversity.ac.in/kalsee)
- **Fee Structure 2026-27**: [kalingauniversity.ac.in/fee-structure](https://kalingauniversity.ac.in/fee-structure)
- **Scholarships & Financial Aid**: [kalingauniversity.ac.in/scholarship](https://kalingauniversity.ac.in/scholarship)
- **Training & Placement Cell**: [kalingauniversity.ac.in/placements](https://kalingauniversity.ac.in/placements)
- **Research & Publications Portal**: [kalingauniversity.ac.in/research](https://kalingauniversity.ac.in/research)

### Regulatory & Accreditation Bodies
- **UGC (University Grants Commission)**: [ugc.gov.in](https://www.ugc.gov.in/)
- **NAAC (National Assessment and Accreditation Council)**: [naac.gov.in](http://www.naac.gov.in/)
- **CPURC (Chhattisgarh Private Universities Regulatory Commission)**: [cgpurc.in](http://cgpurc.in/)
- **AICTE (All India Council for Technical Education)**: [aicte-india.org](https://www.aicte-india.org/)
- **BCI (Bar Council of India)**: [barcouncilofindia.org](http://www.barcouncilofindia.org/)
- **PCI (Pharmacy Council of India)**: [pci.nic.in](https://www.pci.nic.in/)

### Technology References & Documentation
- **FastAPI Documentation**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com/)
- **Scikit-Learn NLP Guide**: [scikit-learn.org/stable/modules/feature_extraction.html](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction)
- **React 18 Documentation**: [react.dev](https://react.dev/)
- **Vite Guide**: [vitejs.dev](https://vitejs.dev/)
- **MDN Progressive Web Apps**: [developer.mozilla.org/en-US/docs/Web/Progressive_web_apps](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps)
- **Tailwind CSS Documentation**: [tailwindcss.com](https://tailwindcss.com/)

---

*Authored for the Kalinga University AI Chatbot Minor Project.*
