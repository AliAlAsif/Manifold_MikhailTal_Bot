from ..ml.model import load_model
model = load_model()

def ml_predict(market):
    features = [
        market.get("liquidity", 0),
        market.get("trades", 0),
        market.get("creator_score", 0),
        market.get("probability", 50)/100,
    ]
    return float(model.predict([features])[0])
