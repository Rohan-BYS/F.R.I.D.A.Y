---
name: email_deliverability_dmarc_dkim_audit
description: Validates DNS TXT record syntaxes for SPF, DKIM, and DMARC enforcement policies (p=reject/quarantine).
category: marketing
version: 1.0.0
created_at: 2026-09-25 01:38:07
---

# 🧠 Learned Skill: email_deliverability_dmarc_dkim_audit

> Validates DNS TXT record syntaxes for SPF, DKIM, and DMARC enforcement policies (p=reject/quarantine).

## Implementation Code
```python
def audit_email_authentication(spf_record: str, dkim_selector_present: bool, dmarc_record: str) -> dict:
    spf_valid = spf_record.startswith("v=spf1") and ("-all" in spf_record or "~all" in spf_record)
    dmarc_valid = dmarc_record.startswith("v=DMARC1")
    dmarc_policy = "none"
    if "p=reject" in dmarc_record:
        dmarc_policy = "reject"
    elif "p=quarantine" in dmarc_record:
        dmarc_policy = "quarantine"
    enforced = dmarc_policy in ["quarantine", "reject"]
    score = 0
    if spf_valid: score += 35
    if dkim_selector_present: score += 35
    if dmarc_valid and enforced: score += 30
    return {
        "spf_status": "VALID" if spf_valid else "MISCONFIGURED",
        "dkim_status": "DETECTED" if dkim_selector_present else "MISSING",
        "dmarc_policy": dmarc_policy,
        "deliverability_health_score": score,
        "spoofing_protected": score >= 90
    }
```

## Validation Tests
```python
res = audit_email_authentication("v=spf1 include:_spf.google.com ~all", True, "v=DMARC1; p=reject; rua=mailto:d@domain.com")
assert res["deliverability_health_score"] == 100
assert res["spoofing_protected"] is True
```
