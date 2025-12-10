import requests
import time
import os

MANIFOLD_API_URL = "https://api.manifold.markets/v0"


class ManifoldClient:
    """
    Lightweight Manifold API client with:
    - get_all_markets()
    - get_markets_by_creator()
    - place_bet()
    """

    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("MANIFOLD_API_KEY")

    # ----------------------------------------------------------------------
    # GET ALL MARKETS (supports pagination)
    # ----------------------------------------------------------------------
    def get_all_markets(self, limit=500):
        url = f"{MANIFOLD_API_URL}/markets"
        params = {"limit": limit}

        try:
            r = requests.get(url, params=params)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            print("Error fetching all markets:", e)
            return []

    # ----------------------------------------------------------------------
    # GET MARKETS BY CREATOR (used in your main bot pipeline)
    # ----------------------------------------------------------------------
    def get_markets_by_creator(self, username):
        url = f"{MANIFOLD_API_URL}/markets"
        params = {"creator": username, "limit": 500}

        try:
            r = requests.get(url, params=params)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            print(f"Error fetching markets for creator {username}:", e)
            return []

    # ----------------------------------------------------------------------
    # PLACE BET
    # ----------------------------------------------------------------------
    def place_bet(self, market_id, outcome, amount):
        """
        outcome: "YES" or "NO"
        amount: mana (int/float)
        """

        if not self.api_key:
            raise ValueError("MANIFOLD_API_KEY is missing")

        url = f"{MANIFOLD_API_URL}/bet"

        payload = {
            "contractId": market_id,
            "outcome": outcome.upper(),
            "amount": float(amount),
        }

        headers = {"Authorization": f"Key {self.api_key}"}

        for attempt in range(3):
            try:
                r = requests.post(url, json=payload, headers=headers)
                if r.status_code == 429:
                    print("Rate limited. Retrying in 2s...")
                    time.sleep(2)
                    continue

                r.raise_for_status()
                return r.json()

            except Exception as e:
                print(f"Bet attempt {attempt+1}/3 failed:", e)
                time.sleep(1)

        print("Bet failed permanently.")
        return None
