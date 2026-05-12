import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
import joblib
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

DATASET_DIR = ROOT_DIR / "dataset"
MODELS_DIR  = ROOT_DIR / "models"
OUTPUTS_DIR = ROOT_DIR / "outputs"
MODELS_DIR.mkdir(exist_ok=True)
OUTPUTS_DIR.mkdir(exist_ok=True)

FEATURE_COLS = ['nitrogen', 'phosphorus', 'potassium', 'ph', 'ec', 'moisture', 'temperature']

def train_scientific_models():
    data_path = DATASET_DIR / "coconut_soil_zone_dataset.csv"
    if not data_path.exists():
        print("Dataset not found. Run data_generator.py first.")
        return

    df = pd.read_csv(data_path)
    X = df[FEATURE_COLS]

    
    print("\n--- Training Stability Model (Decision Support) ---")
    y_stability = df['status']
    X_train, X_test, y_train, y_test = train_test_split(X, y_stability, test_size=0.2, random_state=42)

    model_stability = RandomForestClassifier(n_estimators=100, random_state=42)
    model_stability.fit(X_train, y_train)
    acc = accuracy_score(y_test, model_stability.predict(X_test))
    print(f"Stability Accuracy: {acc:.4f}")

    
    print("--- Training Imbalance Detection Model ---")
    y_imbalance = df['imbalance_type']
    le = LabelEncoder()
    y_encoded = le.fit_transform(y_imbalance)

    X_train2, X_test2, y_train2, y_test2 = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
    model_imbalance = RandomForestClassifier(n_estimators=100, random_state=42)
    model_imbalance.fit(X_train2, y_train2)
    
    y_pred2 = model_imbalance.predict(X_test2)
    acc2 = accuracy_score(y_test2, y_pred2)
    print(f"Imbalance Detection Accuracy: {acc2:.4f}")
    
    
    unique_labels = np.unique(np.concatenate([y_test2, y_pred2]))
    target_names = [le.classes_[i] for i in unique_labels]
    print(classification_report(y_test2, y_pred2, target_names=target_names, zero_division=0))

    
    joblib.dump(model_stability, MODELS_DIR / "stability_model.joblib")
    joblib.dump(model_imbalance, MODELS_DIR / "imbalance_model.joblib")
    joblib.dump(le, MODELS_DIR / "imbalance_label_encoder.joblib")
    joblib.dump({'features': FEATURE_COLS}, MODELS_DIR / "metadata.joblib")

    print("\nScientific Refactoring: Models saved to /models")

if __name__ == "__main__":
    train_scientific_models()
