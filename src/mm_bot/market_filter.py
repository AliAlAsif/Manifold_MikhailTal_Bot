def filter_markets(markets):
    """Only keep binary active markets."""
    result = []
    for m in markets:
        if m.get("outcomeType") != "BINARY":
            continue
        if not m.get("isResolved"):
            result.append(m)
    return result
