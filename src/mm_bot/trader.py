from .client import ManifoldClient

class Trader:

    def __init__(self, simulate=True):
        self.simulate = simulate
        self.client = ManifoldClient()

    def trade(self, trade_decision):
        if trade_decision is None:
            return None

        contract_id, direction, amt = trade_decision

        if self.simulate:
            print(f"[SIM] Buy {direction} {amt} on {contract_id}")
            return {"status": "simulated"}

        print(f"[LIVE] Executing {direction} {amt} on {contract_id}")
        return self.client.place_bet(contract_id, direction, amt)
