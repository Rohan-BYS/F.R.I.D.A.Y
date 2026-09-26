---
name: home_preventative_maintenance_tracker
description: Calculates replacement and service schedules for HVAC, water filters, smoke alarms, and major home appliances.
category: daily_life
version: 1.0.0
created_at: 2026-09-25 01:38:03
---

# 🧠 Learned Skill: home_preventative_maintenance_tracker

> Calculates replacement and service schedules for HVAC, water filters, smoke alarms, and major home appliances.

## Implementation Code
```python
def audit_home_maintenance(items_last_serviced_days: dict) -> list:
    thresholds = {
        "hvac_air_filter": 90,
        "water_purifier_filter": 180,
        "smoke_detector_battery": 365,
        "refrigerator_coil_cleaning": 180,
        "dryer_vent_cleaning": 365,
        "water_heater_flush": 365
    }
    alerts = []
    for item, days in items_last_serviced_days.items():
        limit = thresholds.get(item, 180)
        status = "OK" if days < limit else ("OVERDUE" if days > limit else "DUE_NOW")
        days_remaining = max(0, limit - days)
        alerts.append({
            "item": item,
            "days_since_service": days,
            "interval_limit_days": limit,
            "status": status,
            "days_until_due": days_remaining
        })
    return sorted(alerts, key=lambda x: x["days_until_due"])
```

## Validation Tests
```python
res = audit_home_maintenance({"hvac_air_filter": 100, "smoke_detector_battery": 30})
assert res[0]["item"] == "hvac_air_filter"
assert res[0]["status"] == "OVERDUE"
```
