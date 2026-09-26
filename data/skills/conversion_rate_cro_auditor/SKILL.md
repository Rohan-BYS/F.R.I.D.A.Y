---
name: conversion_rate_cro_auditor
description: Calculates page friction score, social proof density, and Call To Action (CTA) velocity.
category: marketing
version: 1.0.0
created_at: 2026-09-25 01:38:04
---

# 🧠 Learned Skill: conversion_rate_cro_auditor

> Calculates page friction score, social proof density, and Call To Action (CTA) velocity.

## Implementation Code
```python
def audit_conversion_funnel(page_elements: dict) -> dict:
    cta_count = page_elements.get("cta_count", 0)
    has_hero_cta = page_elements.get("has_above_the_fold_cta", False)
    testimonials_count = page_elements.get("testimonials_count", 0)
    form_fields = page_elements.get("form_fields_count", 5)
    has_money_back_guarantee = page_elements.get("has_guarantee", False)
    # Friction calculation: each extra form field increases friction
    friction_score = max(0, (form_fields - 3) * 15)
    cro_score = 0
    if has_hero_cta: cro_score += 25
    if 2 <= cta_count <= 5: cro_score += 25
    if testimonials_count >= 3: cro_score += 25
    if has_money_back_guarantee: cro_score += 25
    final_score = max(0, cro_score - friction_score)
    return {
        "cro_readiness_score": final_score,
        "friction_penalty": friction_score,
        "recommendation": "OPTIMAL" if final_score >= 75 else "REDUCE_FORM_FIELDS_OR_ADD_PROOF"
    }
```

## Validation Tests
```python
res = audit_conversion_funnel({"cta_count": 3, "has_above_the_fold_cta": True, "testimonials_count": 4, "form_fields_count": 2, "has_guarantee": True})
assert res["cro_readiness_score"] == 100
assert res["recommendation"] == "OPTIMAL"
```
