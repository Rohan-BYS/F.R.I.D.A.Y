---
name: central_pivot_range_cpr_intraday
display_name: Central Pivot Range (CPR) & Floor Pivots
category: Technical Analysis
version: 1.0.0
description: Calculates Pivot, Top Central (TC), Bottom Central (BC). Detects Narrow CPR (Trending/Breakout day) and Wide CPR (Range-bound day).
---

# Central Pivot Range (CPR) & Floor Pivots

## Overview
Calculates Pivot, Top Central (TC), Bottom Central (BC). Detects Narrow CPR (Trending/Breakout day) and Wide CPR (Range-bound day).

## Category
**Technical Analysis**

## Architecture & Logic
```python
def calculate_cpr(high, low, close):
    pivot = (high + low + close) / 3.0
    bc = (high + low) / 2.0
    tc = (pivot - bc) + pivot
    cpr_width_pct = abs(tc - bc) / pivot * 100
    # Width < 0.25% indicates high probability of explosive directional trend day
    return {"pivot": pivot, "tc": tc, "bc": bc, "width_pct": cpr_width_pct}
```

## Operational Guidelines
1. Execute autonomously during market hours or on scheduled triggers.
2. Store execution observations in `friday_state.db` and log relevant findings to Market Chronos Excel workbooks.
3. Validate all data with sanity checks to avoid acting on bad ticks or distorted exchange feeds.
