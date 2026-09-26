---
name: options_iron_condor_payoff_matrix
description: Calculates maximum profit, maximum loss, breakeven strikes, and return on risk for an Options Iron Condor.
category: investments
version: 1.0.0
created_at: 2026-09-25 01:41:44
---

# 🧠 Learned Skill: options_iron_condor_payoff_matrix

> Calculates maximum profit, maximum loss, breakeven strikes, and return on risk for an Options Iron Condor.

## Implementation Code
```python
def calculate_iron_condor(put_buy_strike: float, put_sell_strike: float, call_sell_strike: float, call_buy_strike: float, net_credit_received: float) -> dict:
    wing_width = put_sell_strike - put_buy_strike
    max_profit = net_credit_received * 100.0
    max_loss = (wing_width - net_credit_received) * 100.0
    lower_breakeven = put_sell_strike - net_credit_received
    upper_breakeven = call_sell_strike + net_credit_received
    return_on_risk = (max_profit / max_loss) * 100.0 if max_loss > 0 else 0.0
    return {
        "max_profit_usd": round(max_profit, 2),
        "max_loss_usd": round(max_loss, 2),
        "lower_breakeven": round(lower_breakeven, 2),
        "upper_breakeven": round(upper_breakeven, 2),
        "return_on_risk_pct": round(return_on_risk, 2),
        "profit_zone": f"Between ${lower_breakeven} and ${upper_breakeven}"
    }
```

## Validation Tests
```python
res = calculate_iron_condor(90.0, 95.0, 105.0, 110.0, 1.50)
assert res["max_profit_usd"] == 150.0
assert res["max_loss_usd"] == 350.0
assert res["lower_breakeven"] == 93.50
```
