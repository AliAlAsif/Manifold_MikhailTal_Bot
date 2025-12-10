# src/mm_bot/strategy.py
from .ensemble import EnsembleDecisionMaker

# Build a reusable strategy function
def make_strategy(use_openai=True, use_ml=True, weights=None):
    ens = EnsembleDecisionMaker(weights=weights, use_openai=use_openai, use_ml=use_ml)
    def strategy(market):
        return ens.evaluate_market(market)  # returns None or (outcome, stake, rationale)
    return strategy
