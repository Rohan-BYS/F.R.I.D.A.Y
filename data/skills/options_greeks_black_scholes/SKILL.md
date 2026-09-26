---
name: options_greeks_black_scholes
description: Calculates Black-Scholes European call/put theoretical value, delta, and risk-free cost of carry.
category: investments
version: 1.0.0
created_at: 2026-09-25 01:38:07
---

# 🧠 Learned Skill: options_greeks_black_scholes

> Calculates Black-Scholes European call/put theoretical value, delta, and risk-free cost of carry.

## Implementation Code
```python
def calculate_options_pricing(s: float, k: float, t_years: float, r: float, sigma: float) -> dict:
    import math
    if t_years <= 0 or sigma <= 0:
        return {"error": "Invalid time or volatility"}
    d1 = (math.log(s / k) + (r + 0.5 * sigma ** 2) * t_years) / (sigma * math.sqrt(t_years))
    d2 = d1 - sigma * math.sqrt(t_years)
    def norm_cdf(x):
        return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0
    call_price = s * norm_cdf(d1) - k * math.exp(-r * t_years) * norm_cdf(d2)
    put_price = k * math.exp(-r * t_years) * norm_cdf(-d2) - s * norm_cdf(-d1)
    call_delta = norm_cdf(d1)
    put_delta = call_delta - 1.0
    return {
        "call_theoretical_price": round(call_price, 2),
        "put_theoretical_price": round(put_price, 2),
        "call_delta": round(call_delta, 3),
        "put_delta": round(put_delta, 3)
    }
```

## Validation Tests
```python
res = calculate_options_pricing(100.0, 100.0, 1.0, 0.05, 0.20)
assert res["call_theoretical_price"] > 0
assert 0.0 < res["call_delta"] < 1.0
```
