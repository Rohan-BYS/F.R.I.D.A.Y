---
name: forex_pip_value_lot_sizer
description: Calculates pip values, stop loss risk in dollars, and exact standard/mini/micro lot sizes for FX pairs.
category: investments
version: 1.0.0
created_at: 2026-09-25 01:41:45
---

# 🧠 Learned Skill: forex_pip_value_lot_sizer

> Calculates pip values, stop loss risk in dollars, and exact standard/mini/micro lot sizes for FX pairs.

## Implementation Code
```python
def calculate_forex_lot_size(account_equity: float, risk_percent: float, stop_loss_pips: float, pair: str = "EURUSD", exchange_rate: float = 1.0850) -> dict:
    risk_amount_usd = account_equity * (risk_percent / 100.0)
    # For USD quote pairs (e.g., EUR/USD), 1 standard lot (100k units) = $10 per pip
    pip_value_per_standard_lot = 10.0 if pair.endswith("USD") else (10.0 / exchange_rate)
    total_pip_risk = stop_loss_pips * pip_value_per_standard_lot
    standard_lots = risk_amount_usd / total_pip_risk if total_pip_risk > 0 else 0.0
    return {
        "risk_capital_usd": round(risk_amount_usd, 2),
        "stop_loss_pips": stop_loss_pips,
        "standard_lots_100k": round(standard_lots, 2),
        "mini_lots_10k": round(standard_lots * 10.0, 1),
        "micro_lots_1k": round(standard_lots * 100.0, 0)
    }
```

## Validation Tests
```python
res = calculate_forex_lot_size(50000.0, 1.0, 25.0, "EURUSD")
assert res["risk_capital_usd"] == 500.0
assert res["standard_lots_100k"] == 2.0
```
