---
name: bollinger_bands_volatility_squeeze
description: Calculates 20-period Bollinger Bands, bandwidth percentage, and flags high-volatility squeeze breakout setups.
category: investments
version: 1.0.0
created_at: 2026-09-25 01:41:44
---

# 🧠 Learned Skill: bollinger_bands_volatility_squeeze

> Calculates 20-period Bollinger Bands, bandwidth percentage, and flags high-volatility squeeze breakout setups.

## Implementation Code
```python
def calculate_bollinger_bands(closes: list, period: int = 20, num_std: float = 2.0) -> dict:
    if len(closes) < period:
        return {"error": f"Need at least {period} closes"}
    window = closes[-period:]
    sma = sum(window) / period
    variance = sum((x - sma) ** 2 for x in window) / period
    std_dev = variance ** 0.5
    upper = sma + (num_std * std_dev)
    lower = sma - (num_std * std_dev)
    bandwidth = ((upper - lower) / sma) * 100.0 if sma > 0 else 0.0
    current_price = closes[-1]
    # Squeeze is typically identified when bandwidth is compressed below 5%
    is_squeeze = bandwidth < 5.0
    return {
        "middle_band_sma20": round(sma, 2),
        "upper_band": round(upper, 2),
        "lower_band": round(lower, 2),
        "bandwidth_pct": round(bandwidth, 2),
        "volatility_squeeze_active": is_squeeze,
        "trading_signal": "PREPARE_BREAKOUT_PLAY" if is_squeeze else ("UPPER_BAND_RESISTANCE" if current_price >= upper else ("LOWER_BAND_SUPPORT" if current_price <= lower else "NEUTRAL"))
    }
```

## Validation Tests
```python
res = calculate_bollinger_bands([100 + (i % 2) for i in range(25)])
assert res["bandwidth_pct"] < 5.0
assert res["volatility_squeeze_active"] is True
```
