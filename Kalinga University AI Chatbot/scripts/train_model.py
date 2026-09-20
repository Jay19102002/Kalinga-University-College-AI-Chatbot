import os
import sys

backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.nlp.trainer import train_and_save_model

if __name__ == "__main__":
    train_and_save_model()
