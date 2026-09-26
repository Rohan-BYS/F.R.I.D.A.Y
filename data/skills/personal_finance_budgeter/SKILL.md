---
name: personal_finance_budgeter
description: Calculates 50/30/20 budget allocations, discretionary spending limits, and emergency fund runway.
category: daily_life
version: 1.0.0
created_at: 2026-09-25 01:38:03
---

# 🧠 Learned Skill: personal_finance_budgeter

> Calculates 50/30/20 budget allocations, discretionary spending limits, and emergency fund runway.

## Implementation Code
```python
def calculate_budget(monthly_income: float, current_savings: float, monthly_fixed_expenses: float) -> dict:
    needs = monthly_income * 0.50
    wants = monthly_income * 0.30
    savings = monthly_income * 0.20
    discretionary_daily = max(0.0, (wants / 30.0))
    runway_months = (current_savings / monthly_fixed_expenses) if monthly_fixed_expenses > 0 else 0.0
    return {
        "monthly_income": monthly_income,
        "recommended_needs_50pct": round(needs, 2),
        "recommended_wants_30pct": round(wants, 2),
        "recommended_savings_20pct": round(savings, 2),
        "daily_discretionary_budget": round(discretionary_daily, 2),
        "emergency_runway_months": round(runway_months, 2),
        "runway_healthy": runway_months >= 6.0
    }
```

## Validation Tests
```python
res = calculate_budget(5000.0, 15000.0, 2500.0)
assert res["recommended_needs_50pct"] == 2500.0
assert res["emergency_runway_months"] == 6.0
assert res["runway_healthy"] is True
```
