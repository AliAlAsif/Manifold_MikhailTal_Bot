# src/mm_bot/ml/predictor.py
import os
from joblib import load
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.joblib")


class Predictor:
    def __init__(self, model_path: str = MODEL_PATH):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file missing at: {model_path}")
        self.model = load(model_path)
        # classes present in model (e.g. [0] or [0,1])
        self.classes = list(self.model.classes_)

    def extract_features(self, m: dict):
        v24 = float(m.get("volume24Hours") or m.get("volume") or 0)
        liq = float(m.get("liquidity") or m.get("volume") or 0)
        prob = float(m.get("probability") or 0)
        return np.array([[v24, liq, prob]])

    def predict_for_market(self, m):
        liquidity = float(m.get("volume") or 0)
        volume24h = float(m.get("volume24Hours") or 0)
        prob = float(m.get("probability") or 0)

        X = np.array([[liquidity, volume24h, prob]])

        # handle single-class model
        proba = self.model.predict_proba(X)[0]
        proba1 = proba[1] if len(proba) > 1 else float(proba[0])

        label = int(self.model.predict(X)[0])

        return {
            "market": m,  # <‑‑‑‑‑ REQUIRED for main.py
            "label": label,
            "probability": proba1
        }

    def predict_for_markets(self, markets):
        return [self.predict_for_market(m) for m in markets]
