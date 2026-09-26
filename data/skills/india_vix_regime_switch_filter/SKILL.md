---
name: india_vix_regime_switch_filter
display_name: India VIX Volatility Regime Switch
category: Derivatives & Options
version: 1.0.0
description: Analyzes India VIX levels (<12: Complacent, 12-16: Normal Bull, 16-22: Nervous, >22: High Fear) to dictate Option Buying vs Selling strategies.
---

# India VIX Volatility Regime Switch

## Overview
Analyzes India VIX levels (<12: Complacent, 12-16: Normal Bull, 16-22: Nervous, >22: High Fear) to dictate Option Buying vs Selling strategies.

## Category
**Derivatives & Options**

## Architecture & Logic
```python
def get_vix_regime_recommendation(vix_value):
    # Low VIX: Net Credit spreads / Theta decay strategies.
    # Rising VIX: Long Gamma / Momentum breakout buying strategies.
    pass
```

## Operational Guidelines
1. Execute autonomously during market hours or on scheduled triggers.
2. Store execution observations in `friday_state.db` and log relevant findings to Market Chronos Excel workbooks.
3. Validate all data with sanity checks to avoid acting on bad ticks or distorted exchange feeds.
