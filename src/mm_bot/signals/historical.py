def historical_signal(market):
    if "creator_score" not in market: return 0.5
    score = market["creator_score"]
    return min(max(score, 0.1), 0.9)
