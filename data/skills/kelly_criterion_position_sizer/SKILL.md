---
name: kelly_criterion_position_sizer
description: Calculates optimal mathematical capital allocation per trade using the Kelly Criterion and Half-Kelly safety buffers.
category: investments
version: 1.0.0
created_at: 2026-09-25 01:41:44
---

# 🧠 Learned Skill: kelly_criterion_position_sizer

> Calculates optimal mathematical capital allocation per trade using the Kelly Criterion and Half-Kelly safety buffers.

## Implementation Code
```python
def calculate_kelly_position(account_balance: float, win_rate_pct: float, risk_reward_ratio: float, use_half_kelly: bool = True) -> dict:
    p = win_rate_pct / 100.0
    q = 1.0 - p
    b = risk_reward_ratio # Odds received on the wager (Reward / Risk)
    if b <= 0:
        return {"error": "Risk-reward ratio must be greater than 0"}
    # Kelly % = (b*p - q) / b
    kelly_pct = ((b * p) - q) / b
    if kelly_pct <= 0:
        return {
            "recommended_allocation_pct": 0.0,
            "recommended_wager_usd": 0.0,
            "edge_status": "NEGATIVE_EXPECTANCY_DO_NOT_TRADE"
        }
    applied_pct = (kelly_pct / 2.0) if use_half_kelly else kelly_pct
    wager_amount = account_balance * applied_pct
    return {
        "full_kelly_pct": round(kelly_pct * 100.0, 2),
        "applied_allocation_pct": round(applied_pct * 100.0, 2),
        "recommended_position_risk_usd": round(wager_amount, 2),
        "edge_status": "POSITIVE_EXPECTANCY"
    }
```

## Validation Tests
```python
res = calculate_kelly_position(100000.0, 55.0, 2.0, True)
assert res["applied_allocation_pct"] > 0.0
assert res["edge_status"] == "POSITIVE_EXPECTANCY"
```
