---
name: crisis_pr_backlash_velocity_evaluator
description: Calculates social media negative mention velocity and determines whether a public corporate apology is warranted.
category: social_media
version: 1.0.0
created_at: 2026-09-25 01:38:09
---

# 🧠 Learned Skill: crisis_pr_backlash_velocity_evaluator

> Calculates social media negative mention velocity and determines whether a public corporate apology is warranted.

## Implementation Code
```python
def evaluate_pr_crisis(negative_mentions_per_hour: int, baseline_hourly_mentions: int, influencer_involvement: bool, main_press_pickup: bool) -> dict:
    ratio = (negative_mentions_per_hour / baseline_hourly_mentions) if baseline_hourly_mentions > 0 else 10.0
    threat_points = 0
    if ratio >= 5.0: threat_points += 30
    if ratio >= 10.0: threat_points += 20
    if influencer_involvement: threat_points += 25
    if main_press_pickup: threat_points += 25
    action = "STAND_DOWN_DO_NOT_FEED_CYCLE"
    if threat_points >= 75:
        action = "ISSUE_IMMEDIATE_CEO_STATEMENT"
    elif threat_points >= 40:
        action = "PREPARE_HOLDING_STATEMENT_AND_MONITOR"
    return {
        "spike_multiplier": round(ratio, 1),
        "crisis_threat_score": threat_points,
        "recommended_pr_action": action
    }
```

## Validation Tests
```python
res = evaluate_pr_crisis(500, 20, True, True)
assert res["crisis_threat_score"] == 100
assert res["recommended_pr_action"] == "ISSUE_IMMEDIATE_CEO_STATEMENT"
```
