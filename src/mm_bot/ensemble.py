# src/mm_bot/ensemble.py

from .signals.historical import HistoricalSignal
from .signals.microstructure import MicrostructureSignal
from .signals.openai_signal import OpenAISignal
from .signals.ml_signal import MLSignal

class EnsembleDecisionMaker:
    def __init__(self, use_openai=True, use_ml=True):
        self.historical = HistoricalSignal(weight=0.20)
        self.micro = MicrostructureSignal(weight=0.10)
        self.openai = OpenAISignal(weight=0.45) if use_openai else None
        self.ml = MLSignal(weight=0.25) if use_ml else None  # <= ML ADDED

    def predict(self, market_data):
        signals = []
        weights = 0

        # collect signals
        h = self.historical.get_prediction(market_data)
        signals.append(h["prob"] * self.historical.weight)
        weights += self.historical.weight

        m = self.micro.get_prediction(market_data)
        signals.append(m["prob"] * self.micro.weight)
        weights += self.micro.weight

        if self.openai:
            o = self.openai.get_prediction(market_data)
            signals.append(o["prob"] * self.openai.weight)
            weights += self.openai.weight

        if self.ml:
            ml = self.ml.get_prediction(market_data)   # <= ML INCLUDED
            signals.append(ml["prob"] * self.ml.weight)
            weights += self.ml.weight

        final_prob = sum(signals) / weights

        return {
            "final_probability": final_prob,
            "signals": {
                "historical": h,
                "microstructure": m,
                "openai": o if self.openai else None,
                "machine_learning": ml if self.ml else None
            }
        }
