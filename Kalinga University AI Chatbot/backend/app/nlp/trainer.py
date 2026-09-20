import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, f1_score
from app.nlp.preprocessing import normalize_text

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "models")
DATASET_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "data", "processed", "faq_dataset.json")

def train_and_save_model(dataset_path: str = DATASET_FILE, model_dir: str = MODEL_DIR):
    os.makedirs(model_dir, exist_ok=True)
    
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset not found at {dataset_path}")
        
    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    df = pd.DataFrame(data)
    df["clean_question"] = df["question"].apply(normalize_text)
    
    X = df["clean_question"]
    y = df["intent"]
    
    # Label encoding
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True, min_df=1)
    X_tfidf = vectorizer.fit_transform(X)
    
    # Logistic Regression Classifier for smooth probability estimation
    classifier = LogisticRegression(C=10.0, max_iter=1000, random_state=42)
    classifier.fit(X_tfidf, y_encoded)
    
    # Evaluate on training data
    y_pred = classifier.predict(X_tfidf)
    acc = accuracy_score(y_encoded, y_pred)
    macro_f1 = f1_score(y_encoded, y_pred, average="macro")
    
    print(f"=== Model Training Evaluation ===")
    print(f"Total Training Samples: {len(df)}")
    print(f"Unique Intent Classes: {len(label_encoder.classes_)}")
    print(f"Training Accuracy: {acc * 100:.2f}%")
    print(f"Macro F1 Score: {macro_f1 * 100:.2f}%")
    
    # Save artifacts
    joblib.dump(vectorizer, os.path.join(model_dir, "tfidf_vectorizer.joblib"))
    joblib.dump(classifier, os.path.join(model_dir, "intent_classifier.joblib"))
    joblib.dump(label_encoder, os.path.join(model_dir, "label_encoder.joblib"))
    
    print(f"Model artifacts successfully saved to {model_dir}")
    return acc, macro_f1

if __name__ == "__main__":
    train_and_save_model()
