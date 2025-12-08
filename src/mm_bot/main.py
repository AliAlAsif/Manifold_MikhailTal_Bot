import argparse
from .client import ManifoldClient
from .market_filter import filter_markets
from .strategy import baseline_strategy
from .trader import Trader

def run(simulate=True):
    client = ManifoldClient()
    trader = Trader(simulate=simulate)

    markets = client.get_markets_by_user("MikhailTal")
    markets = filter_markets(markets)

    for m in markets:
        decision = baseline_strategy(m)
        trader.trade(decision)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true")
    args = parser.parse_args()

    run(simulate=not args.live)
