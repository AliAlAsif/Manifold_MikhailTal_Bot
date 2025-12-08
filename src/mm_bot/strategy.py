def baseline_strategy(market):
    """Simple probability edge approach."""
    prob = market.get("probability")
    contract_id = market.get("id")

    if prob < 0.20:
        return contract_id, "YES", 5
    elif prob > 0.80:
        return contract_id, "NO", 5

    return None
