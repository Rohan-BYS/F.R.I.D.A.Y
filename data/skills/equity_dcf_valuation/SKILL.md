---
name: equity_dcf_valuation
description: Computes Discounted Cash Flow (DCF) enterprise valuation, terminal value, and implied share price.
category: investments
version: 1.0.0
created_at: 2026-09-25 01:38:04
---

# 🧠 Learned Skill: equity_dcf_valuation

> Computes Discounted Cash Flow (DCF) enterprise valuation, terminal value, and implied share price.

## Implementation Code
```python
def calculate_dcf_valuation(fcf_projections: list, terminal_growth_rate: float, wacc: float, net_debt: float, shares_outstanding: float) -> dict:
    pv_fcf = 0.0
    for year, fcf in enumerate(fcf_projections, 1):
        pv_fcf += fcf / ((1 + wacc) ** year)
    final_fcf = fcf_projections[-1]
    terminal_value = (final_fcf * (1 + terminal_growth_rate)) / (wacc - terminal_growth_rate)
    pv_terminal_value = terminal_value / ((1 + wacc) ** len(fcf_projections))
    enterprise_value = pv_fcf + pv_terminal_value
    equity_value = enterprise_value - net_debt
    intrinsic_share_price = equity_value / shares_outstanding if shares_outstanding > 0 else 0.0
    return {
        "pv_fcf_sum": round(pv_fcf, 2),
        "pv_terminal_value": round(pv_terminal_value, 2),
        "enterprise_value": round(enterprise_value, 2),
        "equity_value": round(equity_value, 2),
        "intrinsic_share_price": round(intrinsic_share_price, 2)
    }
```

## Validation Tests
```python
dcf = calculate_dcf_valuation([100.0, 110.0, 121.0, 133.0, 146.0], 0.025, 0.08, 200.0, 50.0)
assert dcf["intrinsic_share_price"] > 0
assert dcf["enterprise_value"] > dcf["equity_value"]
```
