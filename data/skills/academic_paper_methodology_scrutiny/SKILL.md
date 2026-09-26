---
name: academic_paper_methodology_scrutiny
description: Evaluates academic papers for p-hacking risks, sample size adequacy, control group presence, and conflict of interest.
category: research
version: 1.0.0
created_at: 2026-09-25 01:38:03
---

# 🧠 Learned Skill: academic_paper_methodology_scrutiny

> Evaluates academic papers for p-hacking risks, sample size adequacy, control group presence, and conflict of interest.

## Implementation Code
```python
def evaluate_paper_rigor(sample_size: int, has_control_group: bool, is_double_blind: bool, p_value: float, conflict_of_interest_declared: bool) -> dict:
    rigor_points = 0
    flags = []
    if sample_size >= 100:
        rigor_points += 25
    elif sample_size >= 30:
        rigor_points += 15
    else:
        flags.append("Small sample size (N < 30) - high variance")
    if has_control_group:
        rigor_points += 25
    else:
        flags.append("Missing control group - causal inference compromised")
    if is_double_blind:
        rigor_points += 25
    if p_value < 0.01:
        rigor_points += 25
    elif p_value < 0.05:
        rigor_points += 15
    else:
        flags.append("P-value marginal or non-significant (p >= 0.05)")
    if conflict_of_interest_declared:
        rigor_points = max(0, rigor_points - 20)
        flags.append("Industry/Financial Conflict of Interest declared")
    return {
        "scientific_rigor_score": min(100, rigor_points),
        "risk_flags": flags,
        "is_reputable": rigor_points >= 65 and len(flags) <= 1
    }
```

## Validation Tests
```python
res = evaluate_paper_rigor(250, True, True, 0.002, False)
assert res["scientific_rigor_score"] == 100
assert res["is_reputable"] is True
```
