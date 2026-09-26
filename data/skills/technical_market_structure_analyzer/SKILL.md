---
name: technical_market_structure_analyzer
description: Calculates Fair Value Gaps (FVG), Support/Resistance, and Relative Strength Index (RSI).
category: investments
version: 1.0.0
created_at: 2026-09-25 01:38:04
---

# 🧠 Learned Skill: technical_market_structure_analyzer

> Calculates Fair Value Gaps (FVG), Support/Resistance, and Relative Strength Index (RSI).

## Implementation Code
```python
def analyze_market_structure(ohlc_candles: list) -> dict:
    if len(ohlc_candles) < 3:
        return {"error": "Need at least 3 candles"}
    fvgs = []
    for i in range(len(ohlc_candles) - 2):
        c1, c2, c3 = ohlc_candles[i], ohlc_candles[i+1], ohlc_candles[i+2]
        if c3["low"] > c1["high"]:
            fvgs.append({"type": "BULLISH_FVG", "bottom": c1["high"], "top": c3["low"], "index": i+1})
        elif c3["high"] < c1["low"]:
            fvgs.append({"type": "BEARISH_FVG", "top": c1["low"], "bottom": c3["high"], "index": i+1})
    closes = [c["close"] for c in ohlc_candles]
    gains = [max(0.0, closes[i] - closes[i-1]) for i in range(1, len(closes))]
    losses = [max(0.0, closes[i-1] - closes[i]) for i in range(1, len(closes))]
    avg_gain = (sum(gains) / len(gains)) if gains else 0.0
    avg_loss = (sum(losses) / len(losses)) if losses else 0.0001
    rs = avg_gain / avg_loss
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return {
        "current_rsi": round(rsi, 2),
        "is_overbought": rsi >= 70.0,
        "is_oversold": rsi <= 30.0,
        "detected_fvgs": fvgs,
        "support_level": min(c["low"] for c in ohlc_candles),
        "resistance_level": max(c["high"] for c in ohlc_candles)
    }
```

## Validation Tests
```python
candles = [{"high": 100, "low": 90, "close": 95}, {"high": 115, "low": 98, "close": 112}, {"high": 125, "low": 105, "close": 120}]
res = analyze_market_structure(candles)
assert "current_rsi" in res
assert len(res["detected_fvgs"]) >= 1
```
