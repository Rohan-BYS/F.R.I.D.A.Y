---
name: circadian_sleep_cycle_optimizer
description: Calculates 90-minute REM sleep cycles, sleep latency buffers, and ideal bedtime targets to prevent sleep inertia.
category: daily_life
version: 1.0.0
created_at: 2026-09-25 01:38:09
---

# 🧠 Learned Skill: circadian_sleep_cycle_optimizer

> Calculates 90-minute REM sleep cycles, sleep latency buffers, and ideal bedtime targets to prevent sleep inertia.

## Implementation Code
```python
def calculate_sleep_cycles(wake_up_hour: int, wake_up_minute: int, desired_cycles: int = 5) -> dict:
    total_sleep_minutes = desired_cycles * 90
    latency_buffer_minutes = 15
    total_minutes_needed = total_sleep_minutes + latency_buffer_minutes
    wake_total_minutes = (wake_up_hour * 60) + wake_up_minute
    bed_total_minutes = (wake_total_minutes - total_minutes_needed) % (24 * 60)
    bed_hour = bed_total_minutes // 60
    bed_min = bed_total_minutes % 60
    return {
        "wake_up_time": f"{wake_up_hour:02d}:{wake_up_minute:02d}",
        "sleep_cycles_count": desired_cycles,
        "total_sleep_hours": round(total_sleep_minutes / 60.0, 1),
        "recommended_bedtime": f"{bed_hour:02d}:{bed_min:02d}",
        "prevents_grogginess": True
    }
```

## Validation Tests
```python
res = calculate_sleep_cycles(7, 0, 5)
assert res["total_sleep_hours"] == 7.5
assert "recommended_bedtime" in res
```
