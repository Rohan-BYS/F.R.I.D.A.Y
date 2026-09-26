---
name: paid_ad_roas_breakeven_calculator
description: Calculates target Return on Ad Spend (ROAS), Customer Acquisition Cost (CAC), and Customer Lifetime Value (LTV).
category: marketing
version: 1.0.0
created_at: 2026-09-25 01:38:05
---

# 🧠 Learned Skill: paid_ad_roas_breakeven_calculator

> Calculates target Return on Ad Spend (ROAS), Customer Acquisition Cost (CAC), and Customer Lifetime Value (LTV).

## Implementation Code
```python
def calculate_ad_unit_economics(average_order_value: float, gross_margin_percent: float, ad_spend: float, total_conversions: int) -> dict:
    cpa = (ad_spend / total_conversions) if total_conversions > 0 else 0.0
    breakeven_roas = (1.0 / (gross_margin_percent / 100.0)) if gross_margin_percent > 0 else 999.0
    revenue = total_conversions * average_order_value
    current_roas = (revenue / ad_spend) if ad_spend > 0 else 0.0
    profit = (revenue * (gross_margin_percent / 100.0)) - ad_spend
    return {
        "cost_per_acquisition": round(cpa, 2),
        "breakeven_roas_multiplier": round(breakeven_roas, 2),
        "actual_roas_multiplier": round(current_roas, 2),
        "campaign_net_profit": round(profit, 2),
        "is_profitable": profit > 0.0
    }
```

## Validation Tests
```python
res = calculate_ad_unit_economics(100.0, 70.0, 1000.0, 20)
assert res["cost_per_acquisition"] == 50.0
assert res["is_profitable"] is True
```
