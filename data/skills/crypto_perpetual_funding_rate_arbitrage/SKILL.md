---
name: crypto_perpetual_funding_rate_arbitrage
description: Calculates annualized funding yield for cash-and-carry delta neutral arbitrage and flags liquidation squeeze risks.
category: investments
version: 1.0.0
created_at: 2026-09-25 01:41:44
---

# 🧠 Learned Skill: crypto_perpetual_funding_rate_arbitrage

> Calculates annualized funding yield for cash-and-carry delta neutral arbitrage and flags liquidation squeeze risks.

## Implementation Code
```python
def analyze_perpetual_funding(funding_rate_8h_pct: float, open_interest_change_24h_pct: float) -> dict:
    # 3 funding epochs per day (8 hours each) = 1095 epochs per year
    annualized_funding_yield = funding_rate_8h_pct * 3.0 * 365.0
    squeeze_risk = "EXTREME_LONG_SQUEEZE_RISK (Market Overleveraged Long)" if funding_rate_8h_pct > 0.05 else ("EXTREME_SHORT_SQUEEZE_RISK (Negative Funding Cascading)" if funding_rate_8h_pct < -0.02 else "HEALTHY_EQUILIBRIUM")
    return {
        "funding_rate_8h_pct": funding_rate_8h_pct,
        "annualized_delta_neutral_yield_pct": round(annualized_funding_yield, 2),
        "oi_velocity_24h_pct": open_interest_change_24h_pct,
        "liquidation_cascade_risk": squeeze_risk,
        "arbitrage_viable": abs(annualized_funding_yield) >= 12.0
    }
```

## Validation Tests
```python
res = analyze_perpetual_funding(0.03, 15.0)
assert res["annualized_delta_neutral_yield_pct"] > 30.0
assert res["arbitrage_viable"] is True
```
