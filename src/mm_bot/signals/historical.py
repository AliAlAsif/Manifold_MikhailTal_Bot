# src/mm_bot/signals/historical.py
"""
Historical signal placeholder.
Replace with real logic reading creator history / market resolution biases.
"""
def get_historical_signal(market: dict):
    # Example: if creator has 'creator_bias' field use it; else neutral
    bias = market.get("creator_bias")  # expected: prob (0..1)
    if bias is None:
        return {"prob": 0.5, "confidence": 0.0}
    prob = float(bias)
    return {"prob": max(0.0, min(1.0, prob)), "confidence": abs(prob - 0.5) * 2.0}
