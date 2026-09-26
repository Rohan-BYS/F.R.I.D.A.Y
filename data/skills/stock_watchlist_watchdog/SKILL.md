---
name: stock_watchlist_watchdog
display_name: Autonomous Stock Portfolio Watchdog
category: Portfolio Management
version: 1.0.0
description: 24/7 dedicated sentinel on user's custom stock holdings, alerting immediately upon any material news or price anomalies.
---

# Autonomous Stock Portfolio Watchdog

## Overview
24/7 dedicated sentinel on user's custom stock holdings, alerting immediately upon any material news or price anomalies.

## Category
**Portfolio Management**

## Architecture & Logic
```python
def monitor_user_portfolio(symbols_list):
    # Tracks price action, volume surges (>3x average), and news coverage specifically for user's watchlist.
    pass
```

## Operational Guidelines
1. Execute autonomously during market hours or on scheduled triggers.
2. Store execution observations in `friday_state.db` and log relevant findings to Market Chronos Excel workbooks.
3. Validate all data with sanity checks to avoid acting on bad ticks or distorted exchange feeds.
