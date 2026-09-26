---
name: recruitment_interview_scorecard
description: Calculates structured candidate competency scores across Technical Rigor, Problem Solving, and Culture Fit.
category: white_collar
version: 1.0.0
created_at: 2026-09-25 01:38:09
---

# 🧠 Learned Skill: recruitment_interview_scorecard

> Calculates structured candidate competency scores across Technical Rigor, Problem Solving, and Culture Fit.

## Implementation Code
```python
def score_candidate_interview(technical_1_to_5: float, problem_solving_1_to_5: float, communication_1_to_5: float, cultural_alignment_1_to_5: float) -> dict:
    weights = {"tech": 0.40, "problem": 0.30, "comm": 0.15, "culture": 0.15}
    composite_score = (
        technical_1_to_5 * weights["tech"] +
        problem_solving_1_to_5 * weights["problem"] +
        communication_1_to_5 * weights["comm"] +
        cultural_alignment_1_to_5 * weights["culture"]
    )
    decision = "STRONG_HIRE" if composite_score >= 4.2 else ("HIRE" if composite_score >= 3.5 else ("NO_HIRE" if composite_score >= 2.8 else "STRONG_NO_HIRE"))
    return {
        "composite_score_out_of_5": round(composite_score, 2),
        "hiring_recommendation": decision,
        "passes_bar": composite_score >= 3.5
    }
```

## Validation Tests
```python
res = score_candidate_interview(4.5, 4.0, 4.0, 4.5)
assert res["composite_score_out_of_5"] >= 4.0
assert res["hiring_recommendation"] in ["HIRE", "STRONG_HIRE"]
```
