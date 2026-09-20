---
name: nlp-chatbot
description: Methodology for training, evaluating, and serving TF-IDF + LogisticRegression NLP intent classification models.
---

# NLP Chatbot Skill

## Pipeline Steps
1. Text normalization & lowercasing via `preprocessing.py`.
2. TF-IDF vectorization with 1-2 ngrams.
3. Supervised intent classification using scikit-learn.
4. Entity extraction for programs, degree levels, and entrance exams.
5. Session context tracking for multi-turn follow-ups.
6. Confidence thresholding (0.30) with safe fallback generation.
