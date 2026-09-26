---
name: agile_sprint_capacity_planner
description: Calculates sprint velocity headroom, story point allocations, and risk buffers.
category: white_collar
version: 1.0.0
created_at: 2026-09-25 01:38:06
---

# 🧠 Learned Skill: agile_sprint_capacity_planner

> Calculates sprint velocity headroom, story point allocations, and risk buffers.

## Implementation Code
```python
def calculate_sprint_capacity(team_members_count: int, sprint_days: int = 10, daily_hours: float = 6.0, focus_factor: float = 0.75, committed_story_points: int = 40) -> dict:
    gross_hours = team_members_count * sprint_days * daily_hours
    net_capacity_hours = gross_hours * focus_factor
    hours_per_point = 8.0
    recommended_point_capacity = net_capacity_hours / hours_per_point
    overloaded = committed_story_points > recommended_point_capacity
    return {
        "net_capacity_hours": round(net_capacity_hours, 1),
        "recommended_story_points": round(recommended_point_capacity, 1),
        "committed_story_points": committed_story_points,
        "is_overloaded": overloaded,
        "buffer_points_remaining": round(recommended_point_capacity - committed_story_points, 1)
    }
```

## Validation Tests
```python
res = calculate_sprint_capacity(4, 10, 6.0, 0.75, 20)
assert res["is_overloaded"] is False
assert res["recommended_story_points"] > 20
```
