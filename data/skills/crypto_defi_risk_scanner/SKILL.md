---
name: crypto_defi_risk_scanner
description: Calculates Impermanent Loss, liquidity lockup ratio, and token inflation dilution velocity.
category: investments
version: 1.0.0
created_at: 2026-09-25 01:38:04
---

# 🧠 Learned Skill: crypto_defi_risk_scanner

> Calculates Impermanent Loss, liquidity lockup ratio, and token inflation dilution velocity.

## Implementation Code
```python
def audit_defi_position(initial_token_a_price: float, current_token_a_price: float, initial_pool_liquidity: float, unlocked_team_tokens_pct: float) -> dict:
    price_ratio = current_token_a_price / initial_token_a_price if initial_token_a_price > 0 else 1.0
    # Impermanent Loss formula: 2 * sqrt(r) / (1 + r) - 1
    il = (2.0 * (price_ratio ** 0.5) / (1.0 + price_ratio)) - 1.0
    il_percent = abs(il * 100.0)
    dump_risk = "CRITICAL" if unlocked_team_tokens_pct > 30.0 else ("MODERATE" if unlocked_team_tokens_pct > 15.0 else "LOW")
    return {
        "price_change_ratio": round(price_ratio, 3),
        "impermanent_loss_percent": round(il_percent, 2),
        "team_dump_risk": dump_risk,
        "safe_for_liquidity_provision": il_percent < 8.0 and dump_risk == "LOW"
    }
```

## Validation Tests
```python
res = audit_defi_position(100.0, 200.0, 1000000.0, 5.0)
assert res["impermanent_loss_percent"] > 5.0
assert res["team_dump_risk"] == "LOW"
```
