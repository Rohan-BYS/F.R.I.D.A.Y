---
name: project_pert_three_point_estimator
description: Calculates PERT Expected Duration and Standard Deviation from Optimistic, Most Likely, and Pessimistic estimates.
category: white_collar
version: 1.0.0
created_at: 2026-09-25 01:38:08
---

# 🧠 Learned Skill: project_pert_three_point_estimator

> Calculates PERT Expected Duration and Standard Deviation from Optimistic, Most Likely, and Pessimistic estimates.

## Implementation Code
```python
def calculate_pert_estimate(optimistic_days: float, most_likely_days: float, pessimistic_days: float) -> dict:
    # PERT Formula: (O + 4M + P) / 6
    expected_duration = (optimistic_days + 4.0 * most_likely_days + pessimistic_days) / 6.0
    # Standard deviation: (P - O) / 6
    std_dev = (pessimistic_days - optimistic_days) / 6.0
    return {
        "expected_duration_days": round(expected_duration, 2),
        "standard_deviation_days": round(std_dev, 2),
        "confidence_68pct_range": f"{round(expected_duration - std_dev, 1)} - {round(expected_duration + std_dev, 1)} days",
        "confidence_95pct_range": f"{round(expected_duration - 2 * std_dev, 1)} - {round(expected_duration + 2 * std_dev, 1)} days"
    }
```

## Validation Tests
```python
res = calculate_pert_estimate(10.0, 15.0, 26.0)
assert res["expected_duration_days"] == 16.0
assert res["standard_deviation_days"] > 2.0
```
