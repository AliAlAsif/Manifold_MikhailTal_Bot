import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api.manifold.markets/v0"
API_KEY = os.getenv("MANIFOLD_API_KEY")

class ManifoldClient:

    def __init__(self):
        self.session = requests.Session()
        if API_KEY:
            self.session.headers.update({"Authorization": f"Key {API_KEY}"})

    def get_markets_by_user(self, username="MikhailTal"):
        url = f"{API_URL}/markets?creator={username}"
        r = self.session.get(url)
        r.raise_for_status()
        return r.json()

    def place_bet(self, contract_id, outcome, amount):
        payload = {
            "contractId": contract_id,
            "amount": amount,
            "outcome": outcome
        }
        url = f"{API_URL}/bet"
        r = self.session.post(url, json=payload)
        r.raise_for_status()
        return r.json()
