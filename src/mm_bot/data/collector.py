# src/mm_bot/data/collector.py
import csv
from pathlib import Path
from ..client import ManifoldClient

OUT = Path(__file__).parent / "dataset.csv"
SAFE_LIMIT = 500  # don't request more than this from API

def safe_float(v):
    try:
        if v is None or v == "" or str(v).lower() == "nan":
            return 0.0
        return float(v)
    except Exception:
        return 0.0

def collect_dataset(limit: int = SAFE_LIMIT, out_path: str | Path = None, overwrite: bool = True):
    out_path = Path(out_path or OUT)

    client = ManifoldClient()
    limit = min(limit, SAFE_LIMIT)
    print(f"[INFO] Fetching up to {limit} markets from Manifold...")
    markets = client.get_all_markets(limit=limit) or []
    print(f"[INFO] Fetched {len(markets)} markets (raw)")

    rows = []
    for m in markets:
        # Only use markets that are resolved and have a meaningful resolution
        if not m.get("isResolved"):
            continue

        resolution = (m.get("resolution") or "").upper()
        # keep only clear YES/NO (skip CANCEL, N/A)
        if resolution in ("YES", "MKT"):
            label = 1
        elif resolution == "NO":
            label = 0
        else:
            continue

        # feature order: volume24h, liquidity, probability
        volume24h = safe_float(m.get("volume24Hours") or m.get("volume") or 0)
        liquidity = safe_float(m.get("liquidity") or m.get("volume") or 0)
        prob = safe_float(m.get("probability") or 0)

        rows.append([volume24h, liquidity, prob, label])

    mode = "w" if overwrite else "a"
    with open(out_path, mode, newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"[INFO] Saved {len(rows)} resolved rows to {out_path}")
    return len(rows)


if __name__ == "__main__":
    # example: deletes old file if you want a fresh dataset
    collect_dataset(limit=500, overwrite=True)

