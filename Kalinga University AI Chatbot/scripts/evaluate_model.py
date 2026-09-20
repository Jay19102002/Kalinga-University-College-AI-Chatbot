import os
import sys

backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# pyrefly: ignore [missing-import]
import joblib
from app.nlp.preprocessing import normalize_text

MODEL_DIR = os.path.join(backend_dir, "models")

TEST_QUERIES = [
    ("What is the admission process?", "admission_process"),
    ("How can I apply for admission?", "admission_process"),
    ("What entrance exam do I need?", "entrance_exam"),
    ("What is BBA fee?", "course_fee"),
    ("How much does BBA cost?", "course_fee"),
    ("Does the university provide scholarships?", "scholarship"),
    ("What scholarships are available?", "scholarship"),
    ("Does BBA have internships?", "internship"),
    ("Which companies recruit students?", "placement_companies"),
    ("What is the highest package?", "highest_package"),
    ("What is the average package?", "average_package"),
    ("Tell me about KALSEE", "kalsee"),
    ("What is KAL-MAT?", "kalmat"),
    ("Is there hostel facility?", "hostel_fee"),
    ("What is the weather tomorrow?", "unknown")
]

def evaluate():
    vectorizer = joblib.load(os.path.join(MODEL_DIR, "tfidf_vectorizer.joblib"))
    classifier = joblib.load(os.path.join(MODEL_DIR, "intent_classifier.joblib"))
    label_encoder = joblib.load(os.path.join(MODEL_DIR, "label_encoder.joblib"))
    
    correct = 0
    total = len(TEST_QUERIES)
    
    print("=== Evaluating Model on Sample Benchmark Queries ===")
    for query, expected_intent in TEST_QUERIES:
        clean = normalize_text(query)
        vec = vectorizer.transform([clean])
        pred_idx = classifier.predict(vec)[0]
        probs = classifier.predict_proba(vec)[0]
        confidence = probs[pred_idx]
        pred_intent = label_encoder.inverse_transform([pred_idx])[0]
        
        is_correct = (pred_intent == expected_intent) or (confidence < 0.65 and expected_intent == "unknown")
        if is_correct:
            correct += 1
            status = "PASS"
        else:
            status = "FAIL"
            
        print(f"[{status}] Query: '{query}' -> Pred: '{pred_intent}' (Conf: {confidence:.2f}) | Expected: '{expected_intent}'")
        
    accuracy = (correct / total) * 100
    print(f"\nAccuracy on Test Set: {accuracy:.2f}% ({correct}/{total})")

if __name__ == "__main__":
    evaluate()
