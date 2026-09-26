---
name: real_estate_underwriter
description: Calculates Net Operating Income (NOI), Cap Rate, Cash-on-Cash Return, and Debt Service Coverage Ratio (DSCR).
category: investments
version: 1.0.0
created_at: 2026-09-25 01:38:04
---

# 🧠 Learned Skill: real_estate_underwriter

> Calculates Net Operating Income (NOI), Cap Rate, Cash-on-Cash Return, and Debt Service Coverage Ratio (DSCR).

## Implementation Code
```python
def underwrite_property(purchase_price: float, down_payment: float, gross_annual_rent: float, annual_operating_expenses: float, annual_debt_service: float) -> dict:
    noi = gross_annual_rent - annual_operating_expenses
    cap_rate = (noi / purchase_price) * 100.0 if purchase_price > 0 else 0.0
    annual_cash_flow = noi - annual_debt_service
    cash_on_cash = (annual_cash_flow / down_payment) * 100.0 if down_payment > 0 else 0.0
    dscr = noi / annual_debt_service if annual_debt_service > 0 else 999.0
    return {
        "noi": round(noi, 2),
        "cap_rate_percent": round(cap_rate, 2),
        "annual_cash_flow": round(annual_cash_flow, 2),
        "cash_on_cash_return_percent": round(cash_on_cash, 2),
        "dscr": round(dscr, 2),
        "bankable_dscr": dscr >= 1.25
    }
```

## Validation Tests
```python
res = underwrite_property(500000.0, 100000.0, 60000.0, 15000.0, 30000.0)
assert res["noi"] == 45000.0
assert res["cap_rate_percent"] == 9.0
assert res["dscr"] == 1.5
assert res["bankable_dscr"] is True
```
