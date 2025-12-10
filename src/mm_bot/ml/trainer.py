# src/mm_bot/ml/trainer.py
import csv
from pathlib import Path
from joblib import dump
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

DATASET_PATH = Path(__file__).parent.parent / "data" / "dataset.csv"
MODEL_PATH = Path(__file__).parent / "model.joblib"


def train_model():
    print("[INFO] Loading dataset...")
    if not DATASET_PATH.exists():
        print(f"[ERROR] Dataset not found at {DATASET_PATH}")
        return

    rows = []
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for r in reader:
            # Expect exactly 4 columns: volume24h, liquidity, prob, label
            if len(r) < 4:
                continue
            try:
                v24 = float(r[0])
                liq = float(r[1])
                prob = float(r[2])
                label = int(r[3])
                rows.append([v24, liq, prob, label])
            except Exception:
                continue

    if not rows:
        print("[ERROR] No valid rows in dataset (training aborted).")
        return

    data = np.array(rows, dtype=float)
    X = data[:, :3]   # 3 features
    y = data[:, 3].astype(int)

    unique, counts = np.unique(y, return_counts=True)
    dist = dict(zip(unique.tolist(), counts.tolist()))
    print(f"[INFO] Samples: {len(y)}; label distribution: {dist}")

    if len(unique) < 2:
        print("[ERROR] Dataset contains only one class. Collect more resolved markets with both outcomes.")
        return

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    print("[INFO] Training RandomForest...")
    model = RandomForestClassifier(n_estimators=200, random_state=42, class_weight="balanced")
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"[INFO] Training complete — accuracy: {acc:.4f}")

    dump(model, MODEL_PATH)
    print(f"[INFO] Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    train_model()
