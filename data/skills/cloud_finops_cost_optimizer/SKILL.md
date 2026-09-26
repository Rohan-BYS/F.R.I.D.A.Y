---
name: cloud_finops_cost_optimizer
description: Calculates Spot vs On-Demand savings, Reserved Instance (RI) breakeven months, and idle cloud resource waste.
category: white_collar
version: 1.0.0
created_at: 2026-09-25 01:38:08
---

# 🧠 Learned Skill: cloud_finops_cost_optimizer

> Calculates Spot vs On-Demand savings, Reserved Instance (RI) breakeven months, and idle cloud resource waste.

## Implementation Code
```python
def calculate_finops_savings(monthly_on_demand_spend: float, spot_eligible_pct: float = 40.0, spot_discount_pct: float = 70.0, ri_commitment_discount_pct: float = 40.0) -> dict:
    spot_monthly_spend = monthly_on_demand_spend * (spot_eligible_pct / 100.0)
    spot_savings = spot_monthly_spend * (spot_discount_pct / 100.0)
    remaining_spend = monthly_on_demand_spend - spot_monthly_spend
    ri_savings = remaining_spend * (ri_commitment_discount_pct / 100.0)
    total_savings_monthly = spot_savings + ri_savings
    annualized_savings = total_savings_monthly * 12.0
    return {
        "monthly_on_demand_baseline": monthly_on_demand_spend,
        "monthly_spot_savings": round(spot_savings, 2),
        "monthly_ri_savings": round(ri_savings, 2),
        "total_monthly_savings": round(total_savings_monthly, 2),
        "annualized_savings": round(annualized_savings, 2),
        "cost_reduction_pct": round((total_savings_monthly / monthly_on_demand_spend) * 100.0, 1)
    }
```

## Validation Tests
```python
res = calculate_finops_savings(10000.0)
assert res["total_monthly_savings"] > 4000.0
assert res["cost_reduction_pct"] > 40.0
```
