# src/mm_bot/trader.py
"""
Safe, offline-only trade executor.
This does NOT interact with any real-world platforms.
"""

def execute_trade(client, market_id, outcome, amount):
    """
    Pretend to execute a trade — logs only.
    """

    print(f"[SIMULATED TRADE]")
    print(f" Market ID: {market_id}")
    print(f" Outcome:   {outcome}")
    print(f" Amount:    {amount}")
    print(" (No real action performed)\n")

    # For ML training, you may save simulated trades later.
    return {
        "market_id": market_id,
        "outcome": outcome,
        "amount": amount
    }
