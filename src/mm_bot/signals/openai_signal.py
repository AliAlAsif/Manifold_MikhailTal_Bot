from openai import OpenAI
import os

client = OpenAI()


def openai_forecast(market, runs=3):
    results = []
    for _ in range(runs):
        r = client.responses.create(
            model="gpt-4o-mini",
            input=f"Predict probability: {market['question']}. Answer only number 0-1."
        )
        try:
            prob = float(r.output_text.strip())
            results.append(prob)
        except:
            continue

    return sum(results) / len(results) if results else 0.5
