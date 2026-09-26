---
name: schengen_90_180_travel_calculator
description: Calculates remaining legal travel days in the European Schengen Area under the rolling 90/180-day limitation rule.
category: daily_life
version: 1.0.0
created_at: 2026-09-25 01:38:09
---

# 🧠 Learned Skill: schengen_90_180_travel_calculator

> Calculates remaining legal travel days in the European Schengen Area under the rolling 90/180-day limitation rule.

## Implementation Code
```python
def calculate_schengen_allowance(days_spent_in_last_180_days: int) -> dict:
    max_allowed = 90
    remaining_days = max(0, max_allowed - days_spent_in_last_180_days)
    overstay = days_spent_in_last_180_days > max_allowed
    return {
        "days_spent": days_spent_in_last_180_days,
        "legal_days_remaining": remaining_days,
        "is_overstaying": overstay,
        "status": "LEGAL" if not overstay else "OVERSTAY_PENALTY_WARNING",
        "rolling_window_days": 180
    }
```

## Validation Tests
```python
res = calculate_schengen_allowance(65)
assert res["legal_days_remaining"] == 25
assert res["is_overstaying"] is False
```
