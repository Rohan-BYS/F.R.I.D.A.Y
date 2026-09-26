---
name: shopify_aov_cart_recovery_model
description: Models abandoned cart recovery sequence timing, dynamic discount elasticity, and Average Order Value (AOV) cross-sell uplift.
category: marketing
version: 1.0.0
created_at: 2026-09-25 01:47:22
---

# 🧠 Learned Skill: shopify_aov_cart_recovery_model

> Models abandoned cart recovery sequence timing, dynamic discount elasticity, and Average Order Value (AOV) cross-sell uplift.

## Implementation Code
```python
def model_cart_recovery_sequence(cart_value_usd: float, customer_purchase_count: int) -> dict:
    discount_pct = 0.0 if customer_purchase_count >= 3 else (10.0 if cart_value_usd >= 100.0 else 5.0)
    return {
        "cart_value_usd": cart_value_usd,
        "recovery_cadence": [
            {"hour": 1, "channel": "EMAIL_SMS", "discount": "0%", "hook": "Did you leave something behind?"},
            {"hour": 24, "channel": "EMAIL", "discount": f"{discount_pct}%", "hook": "Exclusive limited-time offer for your cart."},
            {"hour": 48, "channel": "SMS_RETARGETING", "discount": f"{discount_pct}%", "hook": "Final 4 hours before your cart expires."}
        ],
        "recommended_post_purchase_upsell_usd": round(cart_value_usd * 0.25, 2),
        "target_cart_recovery_rate_pct": 18.5
    }
```

## Validation Tests
```python
res = model_cart_recovery_sequence(150.0, 1)
assert len(res["recovery_cadence"]) == 3
assert res["recommended_post_purchase_upsell_usd"] == 37.5
```
