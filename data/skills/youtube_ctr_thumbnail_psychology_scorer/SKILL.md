---
name: youtube_ctr_thumbnail_psychology_scorer
description: Scores thumbnail and title combinations for click-through rate (CTR) potential and curiosity gap tension.
category: content
version: 1.0.0
created_at: 2026-09-25 01:38:07
---

# 🧠 Learned Skill: youtube_ctr_thumbnail_psychology_scorer

> Scores thumbnail and title combinations for click-through rate (CTR) potential and curiosity gap tension.

## Implementation Code
```python
def score_youtube_packaging(title: str, thumbnail_has_face: bool, thumbnail_word_count: int, title_curiosity_gap: bool) -> dict:
    title_len = len(title)
    score = 0
    flags = []
    if 35 <= title_len <= 55:
        score += 30
    else:
        flags.append("Title length outside optimal 35-55 characters")
    if title_curiosity_gap:
        score += 30
    else:
        flags.append("Missing tension or curiosity gap in title")
    if thumbnail_has_face:
        score += 20
    if 1 <= thumbnail_word_count <= 4:
        score += 20
    elif thumbnail_word_count > 6:
        flags.append("Too many words on thumbnail (causes visual clutter)")
    return {
        "estimated_ctr_score": score,
        "title_length": title_len,
        "improvement_flags": flags,
        "expected_performance": "VIRAL_POTENTIAL" if score >= 80 else ("SOLID" if score >= 60 else "NEEDS_OPTIMIZATION")
    }
```

## Validation Tests
```python
res = score_youtube_packaging("The Day AI Became Self-Aware", True, 3, True)
assert res["estimated_ctr_score"] == 100
assert res["expected_performance"] == "VIRAL_POTENTIAL"
```
