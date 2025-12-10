#!/usr/bin/env python3
"""
Poll Manifold for newly resolved markets and reconcile trades.
Usage:
  python scripts/reconcile_resolutions.py --since 2025-01-01
This will:
 - fetch resolved markets for your creator
 - read your trades file (performance_data/trades.csv) and mark realized PnL
 - append PnL to performance_data/pnl.csv
"""
import argparse, os, csv, json
from datetime import datetime
from src.mm_bot.client import ManifoldClient
from src.mm_bot.ledger import write_trade, write_pnl

def load_trades(path="performance_data/trades.csv"):
    if not os.path.exists(path):
        return []
    rows = []
    with open(path,"r",encoding="utf8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return rows

def reconcile(creator, api_key=None, since=None):
    client = ManifoldClient(api_key=api_key)
    resolved = client.get_markets_by_creator(creator, limit=200)
    resolved = [m for m in resolved if m.get("isResolved") or m.get("resolved")]
    trades = load_trades()
    # naive reconciliation: for each trade where placed==False (simulated) or placed==True, compute realized result
    for t in trades:
        market_id = t.get("market_id")
        for m in resolved:
            if m.get("id")==market_id:
                # determine win/loss
                resolution = m.get("resolution") or m.get("resolvedResult") or None
                # convert to boolean: True if YES occurred
                yes_happened = bool(resolution is True)
                direction = t.get("decision") or t.get("outcome") or t.get("decision_outcome")
                amount = float(t.get("amount") or 0)
                profit = 0.0
                p = float(m.get("probability",0.5))
                if direction == "YES":
                    profit = (1.0 - p) * (amount / max(p,1e-9)) if yes_happened else -amount
                else:
                    profit = p * (amount / max(1.0 - p,1e-9)) if not yes_happened else -amount
                # write realized trade row
                write_trade({
                    "market_id": market_id,
                    "question": m.get("question"),
                    "outcome": direction,
                    "amount": amount,
                    "mode": "RECONCILED",
                    "result": profit
                })
                # update pnl snapshot
                write_pnl({"bankroll": profit})
    print("Reconciliation complete.")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--since", default=None)
    p.add_argument("--creator", default=os.getenv("CREATOR_USERNAME","MikhailTal"))
    p.add_argument("--api-key", default=os.getenv("MANIFOLD_API_KEY"))
    args = p.parse_args()
    reconcile(args.creator, api_key=args.api_key, since=args.since)
