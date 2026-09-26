---
name: sql_query_performance_anti_pattern_auditor
description: Scans SQL queries for SELECT *, missing LIMIT, leading wildcards in LIKE, and implicit cross joins.
category: white_collar
version: 1.0.0
created_at: 2026-09-25 01:38:08
---

# 🧠 Learned Skill: sql_query_performance_anti_pattern_auditor

> Scans SQL queries for SELECT *, missing LIMIT, leading wildcards in LIKE, and implicit cross joins.

## Implementation Code
```python
def audit_sql_query(query_text: str) -> dict:
    q = query_text.upper()
    anti_patterns = []
    if "SELECT *" in q:
        anti_patterns.append("SELECT_ALL_COLUMNS: Exposes unintended data and defeats index-only scans.")
    if "LIKE '%" in q:
        anti_patterns.append("LEADING_WILDCARD_LIKE: Invalidates B-Tree indexes, forcing sequential table scans.")
    if "JOIN" not in q and "," in q.split("FROM")[-1].split("WHERE")[0]:
        anti_patterns.append("IMPLICIT_CROSS_JOIN: Multiple tables listed in FROM clause without explicit JOIN condition.")
    if "LIMIT" not in q and "SELECT" in q:
        anti_patterns.append("UNBOUNDED_SELECT: Missing LIMIT clause on large analytical dataset.")
    health_score = max(0, 100 - (len(anti_patterns) * 25))
    return {
        "sql_health_score": health_score,
        "anti_patterns_found": anti_patterns,
        "is_production_safe": health_score >= 75
    }
```

## Validation Tests
```python
res = audit_sql_query("SELECT * FROM users WHERE email LIKE '%@gmail.com'")
assert len(res["anti_patterns_found"]) == 2
assert res["is_production_safe"] is False
```
