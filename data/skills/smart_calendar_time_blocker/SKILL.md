---
name: smart_calendar_time_blocker
description: Allocates daily deep work blocks and buffer periods to minimize context-switching fatigue.
category: daily_life
version: 1.0.0
created_at: 2026-09-25 01:38:03
---

# 🧠 Learned Skill: smart_calendar_time_blocker

> Allocates daily deep work blocks and buffer periods to minimize context-switching fatigue.

## Implementation Code
```python
def generate_time_blocks(available_hours: float, deep_work_tasks: list, shallow_tasks: list) -> dict:
    schedule = []
    current_time = 9.0  # 9:00 AM start
    deep_work_total = 0.0
    for task in deep_work_tasks:
        duration = min(task.get("hours", 1.5), 2.0)
        schedule.append({"time": f"{current_time:04.1f}", "type": "DEEP_WORK", "task": task.get("title", "Deep Work"), "duration_h": duration})
        current_time += duration
        deep_work_total += duration
        schedule.append({"time": f"{current_time:04.1f}", "type": "BUFFER_REST", "task": "Cognitive Reset", "duration_h": 0.25})
        current_time += 0.25
    for task in shallow_tasks:
        duration = task.get("hours", 0.5)
        schedule.append({"time": f"{current_time:04.1f}", "type": "SHALLOW_BATCH", "task": task.get("title", "Admin/Email"), "duration_h": duration})
        current_time += duration
    return {
        "total_deep_work_hours": round(deep_work_total, 2),
        "total_schedule_hours": round(current_time - 9.0, 2),
        "schedule": schedule
    }
```

## Validation Tests
```python
blocks = generate_time_blocks(8.0, [{"title": "Write Engine", "hours": 2.0}], [{"title": "Inbox", "hours": 0.5}])
assert blocks["total_deep_work_hours"] == 2.0
assert len(blocks["schedule"]) == 3
```
