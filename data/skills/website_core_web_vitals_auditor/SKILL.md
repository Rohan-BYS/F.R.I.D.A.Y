---
name: website_core_web_vitals_auditor
description: Evaluates Largest Contentful Paint (LCP), Interaction to Next Paint (INP), and Cumulative Layout Shift (CLS) against Google SEO thresholds.
category: marketing
version: 1.0.0
created_at: 2026-09-25 01:47:22
---

# 🧠 Learned Skill: website_core_web_vitals_auditor

> Evaluates Largest Contentful Paint (LCP), Interaction to Next Paint (INP), and Cumulative Layout Shift (CLS) against Google SEO thresholds.

## Implementation Code
```python
def audit_core_web_vitals(lcp_seconds: float, inp_milliseconds: float, cls_score: float) -> dict:
    lcp_status = "GOOD" if lcp_seconds <= 2.5 else ("NEEDS_IMPROVEMENT" if lcp_seconds <= 4.0 else "POOR")
    inp_status = "GOOD" if inp_milliseconds <= 200.0 else ("NEEDS_IMPROVEMENT" if inp_milliseconds <= 500.0 else "POOR")
    cls_status = "GOOD" if cls_score <= 0.1 else ("NEEDS_IMPROVEMENT" if cls_score <= 0.25 else "POOR")
    all_good = lcp_status == "GOOD" and inp_status == "GOOD" and cls_status == "GOOD"
    return {
        "lcp_seconds": lcp_seconds,
        "lcp_rating": lcp_status,
        "inp_milliseconds": inp_milliseconds,
        "inp_rating": inp_status,
        "cls_score": cls_score,
        "cls_rating": cls_status,
        "passes_google_page_experience": all_good,
        "google_search_ranking_advantage": "ENABLED" if all_good else "PENALIZED_BY_PERFORMANCE"
    }
```

## Validation Tests
```python
res = audit_core_web_vitals(1.8, 120.0, 0.04)
assert res["passes_google_page_experience"] is True
assert res["google_search_ranking_advantage"] == "ENABLED"
```
