# src/mm_bot/signals/microstructure.py
"""
Microstructure signal: simple heuristic based on order imbalance or volume.
"""
def get_micro_signal(market: dict):
    # Example: use 'imbalance' in [-1..1] where positive => buy pressure
    imbalance = float(market.get("imbalance", 0.0))
    prob = 0.5 + (imbalance * 0.25)  # tilt by up to +/-0.25
    prob = max(0.0, min(1.0, prob))
    confidence = min(1.0, abs(imbalance))
    return {"prob": prob, "confidence": confidence}
