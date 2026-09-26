---
name: risk_reward_expectancy_calculator
description: Calculates expected monetary value per trade, breakeven required win-rate, and portfolio survival expectancy.
category: investments
version: 1.0.0
created_at: 2026-09-25 01:41:44
---

# 🧠 Learned Skill: risk_reward_expectancy_calculator

> Calculates expected monetary value per trade, breakeven required win-rate, and portfolio survival expectancy.

## Implementation Code
```python
def calculate_trade_expectancy(win_rate_pct: float, avg_win_usd: float, avg_loss_usd: float, num_trades_sample: int = 100) -> dict:
    w = win_rate_pct / 100.0
    l = 1.0 - w
    # Expectancy = (Win% * Avg Win) - (Loss% * Avg Loss)
    expectancy_per_trade = (w * avg_win_usd) - (l * avg_loss_usd)
    # Breakeven win rate = Loss / (Win + Loss)
    breakeven_win_rate = (avg_loss_usd / (avg_win_usd + avg_loss_usd)) * 100.0 if (avg_win_usd + avg_loss_usd) > 0 else 0.0
    projected_net_gain = expectancy_per_trade * num_trades_sample
    return {
        "expectancy_per_trade_usd": round(expectancy_per_trade, 2),
        "breakeven_win_rate_pct": round(breakeven_win_rate, 2),
        "win_rate_safety_margin_pct": round(win_rate_pct - breakeven_win_rate, 2),
        "projected_profit_over_sample": round(projected_net_gain, 2),
        "system_viable": expectancy_per_trade > 0.0
    }
```

## Validation Tests
```python
res = calculate_trade_expectancy(50.0, 300.0, 100.0)
assert res["expectancy_per_trade_usd"] == 100.0
assert res["system_viable"] is True
```
