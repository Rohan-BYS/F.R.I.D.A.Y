---
name: deep_research_cross_verifier
description: Triangulates facts across independent sources and computes an epistemic confidence rating.
category: research
version: 1.0.0
created_at: 2026-09-25 01:38:03
---

# 🧠 Learned Skill: deep_research_cross_verifier

> Triangulates facts across independent sources and computes an epistemic confidence rating.

## Implementation Code
```python
def cross_verify_claim(claim: str, source_observations: list) -> dict:
    if not source_observations:
        return {"claim": claim, "confidence": 0.0, "status": "UNVERIFIED"}
    confirming = sum(1 for s in source_observations if s.get("supports", False))
    refuting = sum(1 for s in source_observations if s.get("refutes", False))
    independent_domains = len(set(s.get("domain", "") for s in source_observations))
    score = (confirming / len(source_observations)) * min(1.0, independent_domains / 3.0)
    if refuting > 0:
        score = max(0.0, score - (refuting * 0.25))
    status = "HIGH_CONFIDENCE" if score >= 0.75 else ("MODERATE" if score >= 0.4 else "UNRELIABLE_OR_CONTESTED")
    return {
        "claim": claim,
        "confirming_sources": confirming,
        "refuting_sources": refuting,
        "unique_domains": independent_domains,
        "epistemic_confidence_score": round(score, 3),
        "status": status
    }
```

## Validation Tests
```python
obs = [{"domain": "arxiv.org", "supports": True}, {"domain": "nature.com", "supports": True}, {"domain": "mit.edu", "supports": True}]
res = cross_verify_claim("Superconductors at STP", obs)
assert res["status"] == "HIGH_CONFIDENCE"
```
