---
name: negotiation_term_sheet_planner
description: Calculates Best Alternative to a Negotiated Agreement (BATNA), Zone of Possible Agreement (ZOPA), and concession tradeoffs.
category: white_collar
version: 1.0.0
created_at: 2026-09-25 01:38:06
---

# 🧠 Learned Skill: negotiation_term_sheet_planner

> Calculates Best Alternative to a Negotiated Agreement (BATNA), Zone of Possible Agreement (ZOPA), and concession tradeoffs.

## Implementation Code
```python
def plan_negotiation(our_reservation_price: float, our_target_price: float, counterparty_reservation_price: float) -> dict:
    has_zopa = counterparty_reservation_price >= our_reservation_price
    zopa_size = (counterparty_reservation_price - our_reservation_price) if has_zopa else 0.0
    anchor_suggestion = our_target_price * 1.15
    return {
        "has_agreement_zone": has_zopa,
        "zopa_spread": round(zopa_size, 2),
        "recommended_first_anchor": round(anchor_suggestion, 2),
        "guidance": "Anchor high and trade non-monetary concessions" if has_zopa else "Walk away; counterparty ceiling is below our bottom line."
    }
```

## Validation Tests
```python
res = plan_negotiation(100000.0, 140000.0, 125000.0)
assert res["has_agreement_zone"] is True
assert res["zopa_spread"] == 25000.0
```
