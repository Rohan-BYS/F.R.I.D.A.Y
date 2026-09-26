---
name: supertrend_ema_confluence_strategy
display_name: Supertrend + 20/50 EMA Trend Confluence
category: Trend Following
version: 1.0.0
description: High-win-rate trend following confluence: buys only when Supertrend(7,3) is Green AND Price is above 20 EMA and 50 EMA.
---

# Supertrend + 20/50 EMA Trend Confluence

## Overview
High-win-rate trend following confluence: buys only when Supertrend(7,3) is Green AND Price is above 20 EMA and 50 EMA.

## Category
**Trend Following**

## Architecture & Logic
```python
def evaluate_supertrend_ema_confluence(df):
    # Eliminates false choppy signals by requiring multi-indicator alignment.
    # Extremely robust for Indian index futures (Nifty/BankNifty) and large-cap swings.
    pass
```

## Operational Guidelines
1. Execute autonomously during market hours or on scheduled triggers.
2. Store execution observations in `friday_state.db` and log relevant findings to Market Chronos Excel workbooks.
3. Validate all data with sanity checks to avoid acting on bad ticks or distorted exchange feeds.
