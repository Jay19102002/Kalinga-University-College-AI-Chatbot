---
name: browser-qa
description: Quality assurance checklist for testing the chatbot UI and API endpoints.
---

# Browser QA Skill

## Checklist
1. Launch backend FastAPI server (`uvicorn app.main:app`).
2. Launch frontend Vite server (`npm run dev`).
3. Verify welcome message and suggested query pills.
4. Test admissions, fees, scholarships, internships, and placement queries.
5. Verify multi-turn context tracking.
6. Verify fallback handling on unknown inputs.
7. Test Knowledge Base modal tabs.
