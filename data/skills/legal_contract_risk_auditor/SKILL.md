---
name: legal_contract_risk_auditor
description: Scans legal agreements for high-liability clauses, perpetual IP assignment, and punitive indemnification.
category: research
version: 1.0.0
created_at: 2026-09-25 01:38:04
---

# 🧠 Learned Skill: legal_contract_risk_auditor

> Scans legal agreements for high-liability clauses, perpetual IP assignment, and punitive indemnification.

## Implementation Code
```python
def audit_contract_clauses(clauses_text: list) -> dict:
    risk_keywords = {
        "INDEMNIFICATION": ["indemnify", "hold harmless", "defend against all claims"],
        "PERPETUAL_IP_ASSIGNMENT": ["irrevocable", "perpetual", "worldwide assignment", "work for hire"],
        "UNLIMITED_LIABILITY": ["no limitation of liability", "consequential damages", "punitive damages"],
        "NON_COMPETE": ["non-compete", "restrain from engaging", "exclusive covenant"],
        "UNILATERAL_MODIFICATION": ["may modify at any time", "sole discretion", "without notice"]
    }
    detected_risks = []
    for clause in clauses_text:
        c_lower = clause.lower()
        for category, triggers in risk_keywords.items():
            for trigger in triggers:
                if trigger in c_lower:
                    detected_risks.append({"category": category, "trigger_phrase": trigger, "excerpt": clause[:120]})
                    break
    risk_score = min(100, len(detected_risks) * 20)
    return {
        "detected_risk_count": len(detected_risks),
        "contract_risk_score": risk_score,
        "high_risk_flag": risk_score >= 60,
        "risks": detected_risks
    }
```

## Validation Tests
```python
clauses = ["The Contractor hereby grants an irrevocable, perpetual, worldwide assignment of all inventions.", "Client shall indemnify and hold harmless the Agency."]
res = audit_contract_clauses(clauses)
assert res["detected_risk_count"] == 2
assert res["high_risk_flag"] is False
```
