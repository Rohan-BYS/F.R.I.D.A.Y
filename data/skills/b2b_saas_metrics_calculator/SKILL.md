---
name: b2b_saas_metrics_calculator
description: Calculates Net Revenue Retention (NRR), CAC Payback Period, and LTV-to-CAC ratio for SaaS businesses.
category: white_collar
version: 1.0.0
created_at: 2026-09-25 01:38:07
---

# 🧠 Learned Skill: b2b_saas_metrics_calculator

> Calculates Net Revenue Retention (NRR), CAC Payback Period, and LTV-to-CAC ratio for SaaS businesses.

## Implementation Code
```python
def calculate_saas_health(mrr_start: float, expansions: float, churn: float, new_customers_acquired: int, sales_marketing_cost: float, arpu_monthly: float, gross_margin_pct: float = 80.0) -> dict:
    nrr = ((mrr_start + expansions - churn) / mrr_start) * 100.0 if mrr_start > 0 else 0.0
    cac = (sales_marketing_cost / new_customers_acquired) if new_customers_acquired > 0 else 0.0
    monthly_gross_profit_per_user = arpu_monthly * (gross_margin_pct / 100.0)
    payback_months = (cac / monthly_gross_profit_per_user) if monthly_gross_profit_per_user > 0 else 999.0
    # Annual churn rate estimate
    churn_pct = (churn / mrr_start) if mrr_start > 0 else 0.05
    lifetime_months = (1.0 / churn_pct) if churn_pct > 0 else 24.0
    ltv = monthly_gross_profit_per_user * lifetime_months
    ltv_to_cac = (ltv / cac) if cac > 0 else 0.0
    return {
        "net_revenue_retention_pct": round(nrr, 2),
        "cac": round(cac, 2),
        "cac_payback_period_months": round(payback_months, 1),
        "ltv_to_cac_ratio": round(ltv_to_cac, 2),
        "is_fundable": nrr >= 110.0 and payback_months <= 12.0 and ltv_to_cac >= 3.0
    }
```

## Validation Tests
```python
res = calculate_saas_health(100000.0, 15000.0, 3000.0, 50, 25000.0, 150.0, 80.0)
assert res["net_revenue_retention_pct"] == 112.0
assert res["is_fundable"] is True
```
