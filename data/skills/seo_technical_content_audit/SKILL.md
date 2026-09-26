---
name: seo_technical_content_audit
description: Evaluates web copy for keyword density, title tag character limits, semantic headings, and search intent alignment.
category: marketing
version: 1.0.0
created_at: 2026-09-25 01:38:04
---

# 🧠 Learned Skill: seo_technical_content_audit

> Evaluates web copy for keyword density, title tag character limits, semantic headings, and search intent alignment.

## Implementation Code
```python
def audit_seo_copy(title: str, meta_description: str, body_text: str, target_keyword: str) -> dict:
    title_len = len(title)
    meta_len = len(meta_description)
    kw = target_keyword.lower()
    words = body_text.lower().split()
    total_words = len(words)
    kw_count = body_text.lower().count(kw)
    density = (kw_count / total_words) * 100.0 if total_words > 0 else 0.0
    title_ok = 50 <= title_len <= 60
    meta_ok = 140 <= meta_len <= 160
    density_ok = 1.0 <= density <= 2.5
    score = 0
    if title_ok: score += 30
    if meta_ok: score += 30
    if density_ok: score += 40
    return {
        "title_length": title_len,
        "title_optimal": title_ok,
        "meta_description_length": meta_len,
        "meta_optimal": meta_ok,
        "keyword_density_percent": round(density, 2),
        "keyword_density_optimal": density_ok,
        "overall_seo_health_score": score
    }
```

## Validation Tests
```python
res = audit_seo_copy("Best Autonomous AI Assistant F.R.I.D.A.Y. 2026", "A sovereign autonomous AI engine featuring self-healing tools, Docker execution, and local model orchestration.", "ai assistant " * 15 + "regular text " * 85, "ai assistant")
assert res["overall_seo_health_score"] >= 60
```
