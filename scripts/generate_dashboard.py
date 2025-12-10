#!/usr/bin/env python3
"""
Generate PNG charts: cumulative PnL, rolling win rate, drawdown.
"""
import os, csv
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

TRADES_CSV = "performance_data/trades.csv"
OUTDIR = "performance_data/plots"

def load_trades(path=TRADES_CSV):
    if not os.path.exists(path):
        return []
    rows=[]
    with open(path,"r",encoding="utf8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return rows

def make_plots():
    rows = load_trades()
    if not rows:
        print("no trades found")
        return
    profits = [float(r.get("result") or 0) for r in rows]
    times = [r.get("timestamp") or "" for r in rows]
    cum = np.cumsum(profits)
    os.makedirs(OUTDIR, exist_ok=True)
    # cumulative PnL
    plt.figure()
    plt.plot(cum)
    plt.title("Cumulative PnL")
    plt.xlabel("Trade #")
    plt.ylabel("PnL")
    plt.grid(True)
    plt.savefig(os.path.join(OUTDIR,"cumulative_pnl.png"))
    plt.close()
    # win rate rolling
    wins = [1 if p>0 else 0 for p in profits]
    window=20
    winrate=[np.mean(wins[max(0,i-window):i+1]) for i in range(len(wins))]
    plt.figure()
    plt.plot(winrate)
    plt.title("Rolling Win Rate")
    plt.savefig(os.path.join(OUTDIR,"rolling_winrate.png"))
    plt.close()
    print("Saved plots to", OUTDIR)

if __name__ == "__main__":
    make_plots()
