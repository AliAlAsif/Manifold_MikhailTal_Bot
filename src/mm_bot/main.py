import argparse
from .client import ManifoldClient
from .ml.predictor import Predictor

def main(limit=5):
    print(f"[INFO] Fetching {limit} markets...")
    client = ManifoldClient()
    markets = client.get_all_markets(limit=limit)
    print(f"[INFO] Loaded {len(markets)} markets")

    predictor = Predictor()
    predictions = predictor.predict_for_markets(markets)

    # FIXED LOOP
    for m, pred in zip(markets, predictions):
        market_name = m.get("question") or m.get("slug") or "Unknown"
        prob_yes = float(pred["probability"])
        label = pred["label"]

        print("\n--- MARKET ---")
        print("Name:", market_name)
        print("Predicted YES probability:", round(prob_yes, 4))
        print("Predicted label:", label)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    main(limit=args.limit)
