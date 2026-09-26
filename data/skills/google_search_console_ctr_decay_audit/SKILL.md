---
name: google_search_console_ctr_decay_audit
description: Audits Google Search Console data to identify keyword cannibalization, decaying rankings, and low-CTR high-impression opportunities.
category: marketing
version: 1.0.0
created_at: 2026-09-25 01:47:21
---

# 🧠 Learned Skill: google_search_console_ctr_decay_audit

> Audits Google Search Console data to identify keyword cannibalization, decaying rankings, and low-CTR high-impression opportunities.

## Implementation Code
```python
def audit_gsc_performance(queries_data: list) -> dict:
    opportunities = []
    cannibalization_warnings = []
    for q in queries_data:
        impressions = q.get("impressions", 0)
        clicks = q.get("clicks", 0)
        position = q.get("position", 50.0)
        ctr = (clicks / impressions * 100.0) if impressions > 0 else 0.0
        # High impression, low CTR in top 10 = Title/Meta copy fix opportunity
        if position <= 10.0 and impressions >= 1000 and ctr < 3.0:
            opportunities.append({
                "query": q.get("query"),
                "impressions": impressions,
                "clicks": clicks,
                "position": round(position, 1),
                "actual_ctr_pct": round(ctr, 2),
                "action": "REWRITE_TITLE_AND_META_DESCRIPTION (High impressions, underperforming CTR)"
            })
        if q.get("distinct_urls_ranking", 1) >= 2 and position <= 20.0:
            cannibalization_warnings.append({
                "query": q.get("query"),
                "ranking_urls_count": q.get("distinct_urls_ranking"),
                "action": "CONSOLIDATE_OR_CANONICALIZE (Multiple pages competing for same search term)"
            })
    return {
        "high_value_ctr_optimization_count": len(opportunities),
        "cannibalization_risks_count": len(cannibalization_warnings),
        "ctr_opportunities": opportunities[:5],
        "cannibalization_risks": cannibalization_warnings[:5]
    }
```

## Validation Tests
```python
data = [{"query": "digital marketing agency", "impressions": 5000, "clicks": 50, "position": 4.2, "distinct_urls_ranking": 1}]
res = audit_gsc_performance(data)
assert res["high_value_ctr_optimization_count"] == 1
assert "REWRITE_TITLE" in res["ctr_opportunities"][0]["action"]
```
