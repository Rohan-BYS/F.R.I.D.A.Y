---
name: lean_manufacturing_takt_time_calc
description: Calculates Takt Time, Cycle Time variance, and worker station headcount requirements for lean assembly lines.
category: blue_collar
version: 1.0.0
created_at: 2026-09-25 01:38:09
---

# 🧠 Learned Skill: lean_manufacturing_takt_time_calc

> Calculates Takt Time, Cycle Time variance, and worker station headcount requirements for lean assembly lines.

## Implementation Code
```python
def calculate_takt_time(net_available_working_seconds_per_shift: float, customer_demand_units_per_shift: int, total_work_content_seconds: float) -> dict:
    if customer_demand_units_per_shift <= 0:
        return {"error": "Invalid customer demand"}
    takt_time_seconds = net_available_working_seconds_per_shift / customer_demand_units_per_shift
    # Theoretical headcount = Total Work Content / Takt Time
    required_operators = total_work_content_seconds / takt_time_seconds if takt_time_seconds > 0 else 1.0
    return {
        "takt_time_seconds": round(takt_time_seconds, 1),
        "total_work_content_seconds": total_work_content_seconds,
        "theoretical_operators_needed": round(required_operators, 1),
        "recommended_station_count": int(-(-required_operators // 1)) # Ceiling division
    }
```

## Validation Tests
```python
res = calculate_takt_time(27000.0, 450, 180.0)
assert res["takt_time_seconds"] == 60.0
assert res["recommended_station_count"] == 3
```
