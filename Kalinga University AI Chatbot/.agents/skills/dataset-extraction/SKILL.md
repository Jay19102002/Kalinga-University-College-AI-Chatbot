---
name: dataset-extraction
description: Instructions for extracting reliable structured information from Kalinga University source material.
---

# Dataset Extraction Skill

## Steps
1. Locate source documents under `data/raw/`.
2. Extract text paragraphs, tables, headings, and URLs using python docx/XML parsing.
3. Identify admissions, courses, fees, scholarships, internships, and placement categories.
4. Preserve exact numeric values without inventing missing data.
5. Flag historical figures vs current 2026-27 intake details.
6. Generate structured JSON datasets (`intents.json`, `faq_dataset.json`, `faq_dataset.csv`).
