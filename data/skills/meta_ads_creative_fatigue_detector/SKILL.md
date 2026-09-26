---
name: meta_ads_creative_fatigue_detector
description: Calculates Ad Frequency vs. CPA degradation curves to flag ad fatigue and determine creative refresh schedules.
category: marketing
version: 1.0.0
created_at: 2026-09-25 01:47:21
---

# 🧠 Learned Skill: meta_ads_creative_fatigue_detector

> Calculates Ad Frequency vs. CPA degradation curves to flag ad fatigue and determine creative refresh schedules.

## Implementation Code
```python
def detect_ad_fatigue(ad_frequency: float, baseline_cpa: float, current_cpa: float, days_running: int) -> dict:
    cpa_increase_pct = ((current_cpa - baseline_cpa) / baseline_cpa) * 100.0 if baseline_cpa > 0 else 0.0
    is_fatigued = ad_frequency >= 2.5 and cpa_increase_pct >= 25.0
    action = "HEALTHY_CREATIVE"
    if ad_frequency >= 3.5:
        action = "CRITICAL_FATIGUE: Rotate creative immediately or expand audience targeting."
    elif is_fatigued:
        action = "EARLY_FATIGUE: Launch A/B test variations with new hook/thumbnail."
    elif days_running >= 30:
        action = "PROACTIVE_REFRESH: Ad running >30 days, prepare fresh creatives."
    return {
        "ad_frequency": ad_frequency,
        "cpa_increase_pct": round(cpa_increase_pct, 1),
        "creative_fatigued": is_fatigued,
        "recommended_action": action
    }
```

## Validation Tests
```python
res = detect_ad_fatigue(2.8, 20.0, 28.0, 14)
assert res["creative_fatigued"] is True
assert "EARLY_FATIGUE" in res["recommended_action"]
```
