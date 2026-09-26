---
name: volume_profile_poc_value_area
display_name: Volume Profile (POC & Value Area High/Low)
category: Auction Market Theory
version: 1.0.0
description: Calculates Point of Control (POC - price level with highest traded volume) and Value Area (VAH/VAL 70% volume distribution).
---

# Volume Profile (POC & Value Area High/Low)

## Overview
Calculates Point of Control (POC - price level with highest traded volume) and Value Area (VAH/VAL 70% volume distribution).

## Category
**Auction Market Theory**

## Architecture & Logic
```python
def calculate_volume_profile(df_trades):
    # Identifies where institutional buyers accumulated versus thin volume rejection areas.
    pass
```

## Operational Guidelines
1. Execute autonomously during market hours or on scheduled triggers.
2. Store execution observations in `friday_state.db` and log relevant findings to Market Chronos Excel workbooks.
3. Validate all data with sanity checks to avoid acting on bad ticks or distorted exchange feeds.
