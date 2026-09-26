---
name: atr_trailing_stop_risk_manager
display_name: Average True Range (ATR) Volatility Trailing Stop
category: Risk Management
version: 1.0.0
description: Dynamic volatility-based stop loss calculation (e.g. 2x ATR(14)) to prevent getting stopped out during normal market breathing.
---

# Average True Range (ATR) Volatility Trailing Stop

## Overview
Dynamic volatility-based stop loss calculation (e.g. 2x ATR(14)) to prevent getting stopped out during normal market breathing.

## Category
**Risk Management**

## Architecture & Logic
```python
def compute_atr_trailing_stop(close, high, low, multiplier=2.0, period=14):
    # Automatically widens stop in high volatility and tightens in low volatility.
    pass
```

## Operational Guidelines
1. Execute autonomously during market hours or on scheduled triggers.
2. Store execution observations in `friday_state.db` and log relevant findings to Market Chronos Excel workbooks.
3. Validate all data with sanity checks to avoid acting on bad ticks or distorted exchange feeds.
