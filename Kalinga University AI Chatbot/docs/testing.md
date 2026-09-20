# Automated & Empirical Testing Documentation

## Test Execution Summary

### 1. Pytest Unit & Integration Suite
- **Command**: `backend\.venv\Scripts\pytest backend/tests/`
- **Results**: `15 passed out of 15 tests (100% PASS)`
- **Modules Tested**:
  - `test_api.py`: GET `/api/health`, POST `/api/chat` with valid payload, empty payload validation (400), and long query length limit.
  - `test_nlp.py`: Intent classification precision across admissions, KALSEE, fees, scholarships, recruiters, and highest package.
  - `test_safety.py`: Zero hallucination verification, safe fee fallback for unlisted programs, qualified package disclosures.
  - `test_context.py`: Multi-turn session context tracking (inheriting fee intent when switching from BBA to MBA).

### 2. Model Training Metrics
- **Command**: `backend\.venv\Scripts\python scripts/train_model.py`
- **Accuracy**: 100.00%
- **Macro F1 Score**: 100.00%
- **Samples**: 248 pattern-response pairs across 33 intent classes.

### 3. Benchmark Query Evaluation
- **Command**: `backend\.venv\Scripts\python scripts/evaluate_model.py`
- **Evaluation Accuracy**: 93.33% (14/15 benchmark test queries correctly classified).

### 4. Live API Endpoint Verification
- **Command**: `backend\.venv\Scripts\python scripts/verify_api_live.py`
- **Status**: Verified live server responses on `http://localhost:8000/api/chat` with active JSON response output and clickable official source URLs.
