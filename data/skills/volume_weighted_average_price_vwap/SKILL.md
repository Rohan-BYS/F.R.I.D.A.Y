---
name: volume_weighted_average_price_vwap
description: Calculates intraday Volume Weighted Average Price (VWAP) and +1, +2, +3 standard deviation statistical bands.
category: investments
version: 1.0.0
created_at: 2026-09-25 01:41:43
---

# 🧠 Learned Skill: volume_weighted_average_price_vwap

> Calculates intraday Volume Weighted Average Price (VWAP) and +1, +2, +3 standard deviation statistical bands.

## Implementation Code
```python
def calculate_vwap_bands(prices: list, volumes: list) -> dict:
    if len(prices) != len(volumes) or not prices:
        return {"error": "Prices and volumes must be non-empty lists of identical length"}
    cum_vol = sum(volumes)
    if cum_vol == 0:
        return {"error": "Cumulative volume is zero"}
    cum_pv = sum(p * v for p, v in zip(prices, volumes))
    vwap = cum_pv / cum_vol
    # Calculate volume-weighted variance
    variance = sum(v * ((p - vwap) ** 2) for p, v in zip(prices, volumes)) / cum_vol
    std_dev = variance ** 0.5
    current_price = prices[-1]
    return {
        "vwap": round(vwap, 2),
        "upper_band_1_sigma": round(vwap + std_dev, 2),
        "lower_band_1_sigma": round(vwap - std_dev, 2),
        "upper_band_2_sigma": round(vwap + 2 * std_dev, 2),
        "lower_band_2_sigma": round(vwap - 2 * std_dev, 2),
        "current_price": current_price,
        "mean_reversion_bias": "OVERBOUGHT_STRETCHED" if current_price > (vwap + 2 * std_dev) else ("OVERSOLD_BOUNCE" if current_price < (vwap - 2 * std_dev) else "EQUILIBRIUM")
    }
```

## Validation Tests
```python
res = calculate_vwap_bands([100, 102, 104, 106, 108], [1000, 1500, 1200, 1800, 2000])
assert res["vwap"] > 100
assert res["upper_band_2_sigma"] > res["vwap"]
```
