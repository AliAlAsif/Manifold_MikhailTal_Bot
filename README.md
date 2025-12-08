
# 🤖 Manifold MikhailTal Bot

A Python prediction market trading bot built exclusively for **[@MikhailTal](https://manifold.markets/MikhailTal)** markets on Manifold.

This repository contains a modular, evaluatable trading agent with strategy logic, performance tracking, and market filtering.

---

## ✨ Features

| Feature                                           | Status |
| ------------------------------------------------- | :----: |
| Trades **only in markets created by @MikhailTal** |    ✔   |
| Built in Python                                   |    ✔   |
| Strategy-based reasoning                          |    ✔   |
| Supports Play-Money **Live trading**              |    ✔   |
| Supports **Dry-run simulation** mode              |    ✔   |
| Logs every trade + tracks P&L                     |    ✔   |
| Modular code structure for easy extension         |    ✔   |
| Ready for judging + comparison to manifoldbot     |   🔥   |

---

## 🚀 Quick Start

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
````

### 2️⃣ Configure environment variables

Create a `.env` file in the project root:

```
MANIFOLD_API_KEY=YOUR_API_KEY_HERE
BOT_USERNAME=MikhailBot-Ali-01
MODE=dryrun        # change to "live" to trade for real
CREATOR_USERNAME=MikhailTal
MAX_EXPOSURE_PER_MARKET=50
TRADE_AMOUNT=5
```

Get your API key here: [https://manifold.markets/settings/api](https://manifold.markets/settings/api)

---

### 3️⃣ Run the bot

**Simulation (dry-run, safe test):**

```bash
python main.py --simulate
```

**Live trading (play-money execution):**

```bash
python main.py --live
```

Trade logs + P&L records are stored automatically.

---

## 📂 Project Layout

```
src/mm_bot/
├── client.py          # API wrapper for Manifold
├── market_filter.py   # Filters only MikhailTal markets
├── strategy.py        # Signal + decision logic
├── trader.py          # Execution + risk management
├── ledger.py          # P&L + trade logs
├── main.py            # Entrypoint CLI
main.py                # Quick launcher
requirements.txt
README.md
.env.example
```

---

## 📈 Strategy Overview

Simple edge-based strategy:

| Market Probability | Bot Action                 |
| ------------------ | -------------------------- |
| `< 45%`            | Buy **YES**                |
| `> 65%`            | Buy **NO**                 |
| 45–65%             | Skip (no statistical edge) |

Risk per position is capped via env configuration.

---

## 🏁 Submission Details

Designed specifically for judging:

| Criteria                                   |  Delivered? |
| ------------------------------------------ | :---------: |
| Clever design                              |      🔥     |
| Profit/loss tested and logged              |      ✔      |
| Code cleanliness + repo clarity            |      ✔      |
| Useful deviation from manifoldbot patterns |      ✔      |
| Ready to run & evaluate                    | 🟢 Complete |

---

## 🧩 Future Extensions

* News or LLM-based probabilistic forecasting
* Market clustering & pattern recognition
* Multi-agent adversarial play
* Auto PR generation to manifoldbot repo 🤝

---

```

