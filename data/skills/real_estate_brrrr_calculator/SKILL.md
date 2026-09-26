---
name: real_estate_brrrr_calculator
description: Models Buy, Rehab, Rent, Refinance, Repeat equity recovery, cash-out proceeds, and infinite return status.
category: investments
version: 1.0.0
created_at: 2026-09-25 01:38:07
---

# 🧠 Learned Skill: real_estate_brrrr_calculator

> Models Buy, Rehab, Rent, Refinance, Repeat equity recovery, cash-out proceeds, and infinite return status.

## Implementation Code
```python
def model_brrrr_deal(purchase_price: float, rehab_cost: float, arv: float, refi_ltv_pct: float = 75.0, monthly_rent: float = 2000.0, monthly_expenses: float = 1200.0) -> dict:
    total_invested = purchase_price + rehab_cost
    max_refi_loan = arv * (refi_ltv_pct / 100.0)
    cash_left_in_deal = max(0.0, total_invested - max_refi_loan)
    cash_pulled_out = min(total_invested, max_refi_loan)
    annual_cash_flow = (monthly_rent - monthly_expenses) * 12.0
    is_infinite = cash_left_in_deal == 0.0 and annual_cash_flow > 0.0
    coc_return = (annual_cash_flow / cash_left_in_deal * 100.0) if cash_left_in_deal > 0 else (999.0 if is_infinite else 0.0)
    return {
        "total_cash_invested": round(total_invested, 2),
        "refinance_loan_proceeds": round(max_refi_loan, 2),
        "capital_left_in_deal": round(cash_left_in_deal, 2),
        "annual_cash_flow": round(annual_cash_flow, 2),
        "cash_on_cash_pct": round(coc_return, 2),
        "infinite_return_achieved": is_infinite
    }
```

## Validation Tests
```python
res = model_brrrr_deal(100000.0, 30000.0, 180000.0, 75.0, 1800.0, 1100.0)
assert res["refinance_loan_proceeds"] == 135000.0
assert res["capital_left_in_deal"] == 0.0
assert res["infinite_return_achieved"] is True
```
