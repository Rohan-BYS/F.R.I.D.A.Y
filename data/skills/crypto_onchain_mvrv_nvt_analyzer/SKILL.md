---
name: crypto_onchain_mvrv_nvt_analyzer
description: Calculates Bitcoin/Ethereum MVRV Z-Score and NVT Ratio to determine macro cycle market tops and generational bottoms.
category: investments
version: 1.0.0
created_at: 2026-09-25 01:41:44
---

# 🧠 Learned Skill: crypto_onchain_mvrv_nvt_analyzer

> Calculates Bitcoin/Ethereum MVRV Z-Score and NVT Ratio to determine macro cycle market tops and generational bottoms.

## Implementation Code
```python
def analyze_onchain_valuation(market_cap_usd: float, realized_cap_usd: float, daily_transaction_volume_usd: float, mvrv_std_dev: float = 1.0) -> dict:
    mvrv_ratio = market_cap_usd / realized_cap_usd if realized_cap_usd > 0 else 1.0
    # MVRV Z-score = (Market Cap - Realized Cap) / StdDev
    mvrv_z_score = (market_cap_usd - realized_cap_usd) / mvrv_std_dev if mvrv_std_dev > 0 else 0.0
    nvt_ratio = market_cap_usd / daily_transaction_volume_usd if daily_transaction_volume_usd > 0 else 0.0
    cycle_phase = "MACRO_TOP_EUPHORIA (High Risk / Take Profits)" if mvrv_ratio >= 3.5 else ("GENERATIONAL_BOTTOM (Deep Value Accumulation)" if mvrv_ratio <= 1.0 else "FAIR_VALUE_EXPANSION")
    return {
        "mvrv_ratio": round(mvrv_ratio, 2),
        "nvt_ratio": round(nvt_ratio, 1),
        "macro_cycle_status": cycle_phase,
        "is_undervalued_historically": mvrv_ratio <= 1.0
    }
```

## Validation Tests
```python
res = analyze_onchain_valuation(500000000.0, 600000000.0, 10000000.0)
assert res["mvrv_ratio"] < 1.0
assert res["is_undervalued_historically"] is True
```
