# src/mm_bot/ensemble.py
from .signals.historical import get_historical_signal
from .signals.microstructure import get_micro_signal
from .signals.openai_signal import OpenAISignal
from .signals.ml_signal import MLSignal
import os

DEFAULT_WEIGHTS = {
    "historical": 0.20,
    "micro": 0.15,
    "openai": 0.35,
    "ml": 0.30
}

class EnsembleDecisionMaker:
    def __init__(self, weights=None, use_openai=True, use_ml=True):
        self.weights = weights or DEFAULT_WEIGHTS.copy()
        self.openai = OpenAISignal() if use_openai else None
        self.ml = MLSignal() if use_ml else None

    def evaluate_market(self, market: dict):
        """
        Returns (outcome, amount, rationale) OR None if low conviction.
        outcome: "YES" or "NO"; amount: recommended stake (float)
        """
        # collect signals
        hist = get_historical_signal(market)
        micro = get_micro_signal(market)
        oai = self.openai.get_signal(market) if self.openai else {"prob": 0.5, "confidence": 0}
        ml = self.ml.get_signal(market) if self.ml else {"prob": 0.5, "confidence": 0}

        # Weighted average using confidence as secondary weight
        signals = {
            "historical": hist,
            "micro": micro,
            "openai": oai,
            "ml": ml
        }

        # normalize weights to sum 1
        w = self.weights.copy()
        total_w = sum(w.values())
        if total_w <= 0:
            # fallback equal weights
            for k in w:
                w[k] = 1.0 / len(w)
        else:
            for k in w:
                w[k] = float(w[k]) / total_w

        # combine: weight * signal_prob * (1 + confidence)
        weighted_sum = 0.0
        denom = 0.0
        for name, s in signals.items():
            prob = float(s.get("prob", 0.5))
            conf = float(s.get("confidence", 0.0))
            factor = w.get(name, 0.0) * (1.0 + conf)  # confidence boosts that signal
            weighted_sum += factor * prob
            denom += factor

        final_prob = weighted_sum / denom if denom > 0 else 0.5

        # market probability - two common field names
        market_prob = market.get("probability")
        if market_prob is None:
            market_prob = market.get("prob") or market.get("market_prob") or 0.5
        market_prob = float(market_prob)

        edge = final_prob - market_prob
        abs_edge = abs(edge)

        # minimum edge threshold (configurable via env)
        min_edge = float(os.getenv("MM_MIN_EDGE", 0.05))

        if abs_edge < min_edge:
            return None

        # Kelly sizing (quarter-Kelly for safety)
        bankroll = float(os.getenv("MM_BANKROLL", 1000.0))
        bet_frac = self._kelly_fraction(final_prob, market_prob)
        bet_frac = max(0.0, min(bet_frac, 0.15))  # cap 15% of bankroll
        bet_frac *= 0.25  # quarter-Kelly
        stake = round(bankroll * bet_frac, 2)

        outcome = "YES" if edge > 0 else "NO"
        rationale = {
            "final_prob": final_prob,
            "market_prob": market_prob,
            "signals": signals,
            "weights": w,
            "edge": edge,
            "stake": stake
        }
        return outcome, stake, rationale

    def _kelly_fraction(self, p, market_p):
        """
        Compute Kelly fraction f* for binary bet where market price = market_p,
        we receive net odds b = (1 - market_p) / market_p for a YES purchase at market price.
        Formula: f* = (b*p - q) / b, where q = 1-p.
        """
        q = 1.0 - p
        if market_p <= 0 or market_p >= 1.0:
            return 0.0
        b = (1.0 - market_p) / market_p
        f = (b * p - q) / b
        return max(0.0, f)
