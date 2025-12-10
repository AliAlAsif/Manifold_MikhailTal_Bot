#!/usr/bin/env python3
"""
Train ML model, run backtest, save model + metrics.
Usage:
  python scripts/retrain.py --data src/mm_bot/data/dataset.csv --out-model src/mm_bot/ml/model.pkl --out-report performance_data/retrain_report.json
"""
import argparse, json, os, sys
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib
from datetime import datetime

# backtest helper (simple)
from src.mm_bot.tools.backtester import simulate_trades_on_history, write_ledger_csv

def train_model(data_csv, model_path):
    df = pd.read_csv(data_csv)
    # Basic feature set - adjust to match your dataset
    features = ["market_prob","volume","liquidity","question_len","question_digits"]
    df = df.dropna(subset=["label"])
    X = df[features].fillna(0)
    y = df["label"].astype(int)
    if len(df) < 50:
        raise RuntimeError("Not enough data to train reliably.")
    model = RandomForestRegressor(n_estimators=200, n_jobs=-1, random_state=42)
    model.fit(X, y)
    os.makedirs(os.path.dirname(model_path) or ".", exist_ok=True)
    joblib.dump({"model": model, "features": features}, model_path)
    return model, features

def run_backtest_and_report(model, features, dataset_csv, out_dir):
    df = pd.read_csv(dataset_csv)
    # create pseudo markets list (must include fields expected by backtester)
    markets = []
    for _, r in df.iterrows():
        markets.append({
            "id": r.get("id", ""),
            "question": r.get("question",""),
            "probability": r.get("market_prob", 0.5),
            "volume": r.get("volume", 0),
            "liquidity": r.get("liquidity", 0),
            "isResolved": True,
            "resolution": bool(r.get("label",0))
        })
    # simple strategy: use model.predict_proba => here approximate by model.predict (regressor)
    def strategy_fn(market):
        feat = [market.get("probability",0.5), market.get("volume",0), market.get("liquidity",0),
                len(market.get("question","")), sum(c.isdigit() for c in (market.get("question","")))]
        try:
            p = model.predict([feat])[0]
        except Exception:
            return None
        edge = p - (market.get("probability",0.5))
        min_edge = 0.05
        if abs(edge) < min_edge:
            return None
        direction = "YES" if edge > 0 else "NO"
        amount = max(1.0, round(abs(edge) * 100.0, 2))
        return (direction, amount)

    res = simulate_trades_on_history(markets, strategy_fn, initial_bankroll=1000.0)
    os.makedirs(out_dir, exist_ok=True)
    write_ledger_csv(res["ledger"], path=os.path.join(out_dir, "retrain_ledger.csv"))
    report = {
        "final_bankroll": res["final_bankroll"],
        "max_drawdown": res["max_drawdown"],
        "timestamp": datetime.utcnow().isoformat()
    }
    return report

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data", default="src/mm_bot/data/dataset.csv")
    p.add_argument("--out-model", default="src/mm_bot/ml/model.pkl")
    p.add_argument("--out-dir", default="performance_data")
    args = p.parse_args()

    if not os.path.exists(args.data):
        print("ERROR: data file not found:", args.data)
        sys.exit(2)

    print("Training model from", args.data)
    model, features = train_model(args.data, args.out_model)
    print("Model saved to", args.out_model)

    print("Running backtest (training-time)")
    report = run_backtest_and_report(model, features, args.data, args.out_dir)
    report_path = os.path.join(args.out_dir, "retrain_report.json")
    with open(report_path,"w",encoding="utf8") as f:
        json.dump(report, f, indent=2)
    print("Retrain report:", report)
    print("Done.")

if __name__ == "__main__":
    main()
