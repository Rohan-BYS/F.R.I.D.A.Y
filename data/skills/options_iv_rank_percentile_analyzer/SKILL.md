---
name: options_iv_rank_percentile_analyzer
description: Calculates Implied Volatility Rank (IV Rank) and IV Percentile to dictate Net Debit vs Net Credit options strategies.
category: investments
version: 1.0.0
created_at: 2026-09-25 01:41:44
---

# 🧠 Learned Skill: options_iv_rank_percentile_analyzer

> Calculates Implied Volatility Rank (IV Rank) and IV Percentile to dictate Net Debit vs Net Credit options strategies.

## Implementation Code
```python
def analyze_iv_environment(current_iv: float, iv_low_52wk: float, iv_high_52wk: float, days_below_current_iv: int, total_trading_days: int = 252) -> dict:
    iv_range = iv_high_52wk - iv_low_52wk
    iv_rank = ((current_iv - iv_low_52wk) / iv_range) * 100.0 if iv_range > 0 else 50.0
    iv_percentile = (days_below_current_iv / total_trading_days) * 100.0 if total_trading_days > 0 else 50.0
    strategy_recommendation = "SELL_PREMIUM (Iron Condor, Credit Spreads, Strangles)" if iv_rank >= 50.0 else "BUY_PREMIUM (Long Calls/Puts, Debit Spreads, Calendar Spreads)"
    return {
        "current_iv": current_iv,
        "iv_rank_pct": round(iv_rank, 1),
        "iv_percentile_pct": round(iv_percentile, 1),
        "volatility_regime": "HIGH_IV (Expensive Options)" if iv_rank >= 50.0 else "LOW_IV (Cheap Options)",
        "optimal_options_play": strategy_recommendation
    }
```

## Validation Tests
```python
res = analyze_iv_environment(65.0, 20.0, 80.0, 200)
assert res["iv_rank_pct"] == 75.0
assert "SELL_PREMIUM" in res["optimal_options_play"]
```
