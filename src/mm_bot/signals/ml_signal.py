# src/mm_bot/signals/ml_signal.py
"""
ML signal: load the trained model and return a probability + confidence.
Assumes model was saved with joblib and supports predict_proba(X).
"""
import os
import joblib
import numpy as np

MODEL_PATH = os.getenv("MM_ML_MODEL", "src/mm_bot/ml/model.pkl")

class MLSignal:
    def __init__(self, model_path: str = MODEL_PATH):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"ML model not found at {model_path}. Train first.")
        self.artifact = joblib.load(model_path)
        # if saved as dict {'model': model, 'features': [...]}
        if isinstance(self.artifact, dict) and "model" in self.artifact:
            self.model = self.artifact["model"]
            self.features = self.artifact.get("features", None)
        else:
            self.model = self.artifact
            self.features = None

    def _market_to_features(self, market: dict):
        """
        Build the feature vector *in the same order* used during training.
        Adapt this to match your trainer features.
        """
        # Example feature vector (change to match your trainer):
        #   liquidity, volume24h, prob (0..1)
        liquidity = float(market.get("liquidity") or 0.0)
        volume = float(market.get("volume24Hours") or market.get("volume") or 0.0)
        prob = float(market.get("probability") or market.get("prob") or 0.0)
        return np.array([liquidity, volume, prob]).reshape(1, -1)

    def get_signal(self, market: dict):
        """Return {'prob': float 0..1, 'confidence': 0..1}"""
        X = self._market_to_features(market)
        try:
            proba = self.model.predict_proba(X)[0][1]
            # confidence heuristic: distance from 0.5 times calibrated score
            confidence = abs(proba - 0.5) * 2.0
            confidence = float(max(0.0, min(1.0, confidence)))
            return {"prob": float(proba), "confidence": confidence}
        except Exception:
            # fallback: return neutral
            return {"prob": 0.5, "confidence": 0.0}
