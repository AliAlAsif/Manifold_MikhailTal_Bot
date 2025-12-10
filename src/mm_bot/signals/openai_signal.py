# src/mm_bot/signals/openai_signal.py
"""
Simple wrapper for your OpenAI signal. Keep calls low-cost in production.
This example returns a neutral 0.5 if OpenAI is disabled or fails.
"""
import os
# If you use openai, import and call; otherwise return neutral
USE_OPENAI = os.getenv("USE_OPENAI", "false").lower() in ("1", "true", "yes")

if USE_OPENAI:
    import openai

class OpenAISignal:
    def __init__(self):
        self.enabled = USE_OPENAI
        if self.enabled:
            openai.api_key = os.getenv("OPENAI_API_KEY")

    def get_signal(self, market: dict):
        if not self.enabled:
            return {"prob": 0.5, "confidence": 0.0}
        try:
            q = market.get("question", market.get("name", ""))
            prompt = f"Give a probability (decimal 0-1) for: {q}\nReply with a single number."
            resp = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=8, temperature=0.0)
            text = resp.choices[0].text.strip()
            p = float(text)
            p = max(0.0, min(1.0, p))
            return {"prob": p, "confidence": abs(p - 0.5) * 2.0}
        except Exception:
            return {"prob": 0.5, "confidence": 0.0}
