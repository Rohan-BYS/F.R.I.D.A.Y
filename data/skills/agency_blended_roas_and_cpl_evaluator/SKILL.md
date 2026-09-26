---
name: agency_blended_roas_and_cpl_evaluator
description: Calculates Marketing Efficiency Ratio (MER / Blended ROAS), Cost Per Lead (CPL), and multi-channel marketing attribution.
category: marketing
version: 1.0.0
created_at: 2026-09-25 01:47:22
---

# 🧠 Learned Skill: agency_blended_roas_and_cpl_evaluator

> Calculates Marketing Efficiency Ratio (MER / Blended ROAS), Cost Per Lead (CPL), and multi-channel marketing attribution.

## Implementation Code
```python
def calculate_agency_blended_metrics(total_ad_spend_all_channels: float, total_revenue_all_channels: float, total_leads_generated: int) -> dict:
    blended_roas = (total_revenue_all_channels / total_ad_spend_all_channels) if total_ad_spend_all_channels > 0 else 0.0
    cpl = (total_ad_spend_all_channels / total_leads_generated) if total_leads_generated > 0 else 0.0
    mer = blended_roas
    health = "EXCELLENT (Scaling Budget Permitted)" if mer >= 3.5 else ("STABLE (Maintain Spend)" if mer >= 2.0 else "UNPROFITABLE (Audit Attribution & CVR)")
    return {
        "blended_roas_mer": round(blended_roas, 2),
        "cost_per_lead_usd": round(cpl, 2),
        "agency_performance_tier": health,
        "is_scaling_recommended": mer >= 3.5
    }
```

## Validation Tests
```python
res = calculate_agency_blended_metrics(10000.0, 42000.0, 250)
assert res["blended_roas_mer"] == 4.2
assert res["cost_per_lead_usd"] == 40.0
assert res["is_scaling_recommended"] is True
```
