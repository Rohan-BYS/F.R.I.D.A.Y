---
name: customer_churn_cohort_analysis
description: Calculates monthly retention cohort percentages, churn rate velocity, and expected customer lifespan.
category: white_collar
version: 1.0.0
created_at: 2026-09-25 01:38:08
---

# 🧠 Learned Skill: customer_churn_cohort_analysis

> Calculates monthly retention cohort percentages, churn rate velocity, and expected customer lifespan.

## Implementation Code
```python
def analyze_churn_cohort(cohort_initial_size: int, active_users_per_month: list) -> dict:
    if cohort_initial_size <= 0:
        return {"error": "Invalid cohort initial size"}
    retention_curve = [round((active / cohort_initial_size) * 100.0, 1) for active in active_users_per_month]
    recent_churn_rate = 0.0
    if len(active_users_per_month) >= 2:
        prev, curr = active_users_per_month[-2], active_users_per_month[-1]
        recent_churn_rate = ((prev - curr) / prev) * 100.0 if prev > 0 else 0.0
    avg_lifespan_months = (100.0 / recent_churn_rate) if recent_churn_rate > 0 else 999.0
    return {
        "initial_cohort_size": cohort_initial_size,
        "retention_curve_pct": retention_curve,
        "latest_monthly_churn_pct": round(recent_churn_rate, 2),
        "expected_customer_lifespan_months": round(avg_lifespan_months, 1)
    }
```

## Validation Tests
```python
res = analyze_churn_cohort(1000, [1000, 850, 750, 700, 680])
assert res["retention_curve_pct"][0] == 100.0
assert res["retention_curve_pct"][-1] == 68.0
```
