---
name: hubspot_lead_scoring_mql_pipeline
description: Calculates behavioral lead scores based on pricing page visits, form submissions, and email engagement to qualify MQL/SQL status.
category: marketing
version: 1.0.0
created_at: 2026-09-25 01:47:22
---

# 🧠 Learned Skill: hubspot_lead_scoring_mql_pipeline

> Calculates behavioral lead scores based on pricing page visits, form submissions, and email engagement to qualify MQL/SQL status.

## Implementation Code
```python
def calculate_lead_score(pricing_page_visits: int, content_downloads: int, email_clicks: int, company_size_headcount: int) -> dict:
    score = 0
    score += min(40, pricing_page_visits * 15)
    score += min(30, content_downloads * 10)
    score += min(20, email_clicks * 5)
    if company_size_headcount >= 50:
        score += 25
    elif company_size_headcount >= 10:
        score += 15
    stage = "SUBSCRIBER"
    if score >= 80:
        stage = "SQL (Sales Qualified Lead - Route to Account Executive)"
    elif score >= 50:
        stage = "MQL (Marketing Qualified Lead - Trigger Automated Nurture Call)"
    elif score >= 25:
        stage = "LEAD (Enrolled in Educational Drip Sequence)"
    return {
        "composite_lead_score": score,
        "lifecycle_stage": stage,
        "ready_for_sales_outreach": score >= 80
    }
```

## Validation Tests
```python
res = calculate_lead_score(3, 2, 4, 100)
assert res["composite_lead_score"] >= 80
assert res["ready_for_sales_outreach"] is True
```
