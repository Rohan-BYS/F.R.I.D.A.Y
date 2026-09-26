---
name: candlestick_pattern_recognition_engine
description: Recognizes reversal candlestick patterns: Bullish/Bearish Engulfing, Hammer, Shooting Star, and Doji.
category: investments
version: 1.0.0
created_at: 2026-09-25 01:41:44
---

# 🧠 Learned Skill: candlestick_pattern_recognition_engine

> Recognizes reversal candlestick patterns: Bullish/Bearish Engulfing, Hammer, Shooting Star, and Doji.

## Implementation Code
```python
def detect_candlestick_pattern(open_p: float, high_p: float, low_p: float, close_p: float, prev_open: float, prev_close: float) -> dict:
    body = abs(close_p - open_p)
    total_range = high_p - low_p if (high_p - low_p) > 0 else 0.0001
    upper_wick = high_p - max(open_p, close_p)
    lower_wick = min(open_p, close_p) - low_p
    is_bullish = close_p > open_p
    prev_bullish = prev_close > prev_open
    pattern = "INDECISION / STANDARD"
    if body / total_range < 0.10:
        pattern = "DOJI (Equilibrium / Impending Volatility)"
    elif lower_wick >= 2.0 * body and upper_wick <= 0.2 * body:
        pattern = "HAMMER (Bullish Reversal Signal at support)"
    elif upper_wick >= 2.0 * body and lower_wick <= 0.2 * body:
        pattern = "SHOOTING_STAR (Bearish Reversal Signal at resistance)"
    elif is_bullish and not prev_bullish and open_p <= prev_close and close_p >= prev_open:
        pattern = "BULLISH_ENGULFING (Strong Institutional Accumulation)"
    elif not is_bullish and prev_bullish and open_p >= prev_close and close_p <= prev_open:
        pattern = "BEARISH_ENGULFING (Strong Institutional Distribution)"
    return {
        "detected_pattern": pattern,
        "is_reversal": pattern != "INDECISION / STANDARD",
        "body_to_range_ratio": round(body / total_range, 3),
        "is_bullish_candle": is_bullish
    }
```

## Validation Tests
```python
res = detect_candlestick_pattern(95.0, 96.0, 70.0, 94.0, 96.0, 95.0)
assert "HAMMER" in res["detected_pattern"]
assert res["is_reversal"] is True
```
