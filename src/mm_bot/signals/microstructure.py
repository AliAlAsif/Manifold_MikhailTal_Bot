def micro_signal(market):
    depth = market.get("order_depth", 1)
    imbalance = market.get("imbalance", 0)

    p = 0.5 + (imbalance / (depth+1)) * 0.4
    return min(max(p, 0.1), 0.9)
