---
name: macro_global_tracker
display_name: Global Macro & Central Bank Tracker
category: Global Macro
version: 1.0.0
description: Monitors US Federal Reserve FOMC decisions, US 10Y Treasury yields, DXY, and geopolitical risk indices for emerging market spillovers.
---

# Global Macro & Central Bank Tracker

## Overview
Monitors US Federal Reserve FOMC decisions, US 10Y Treasury yields, DXY, and geopolitical risk indices for emerging market spillovers.

## Category
**Global Macro**

## Architecture & Logic
```python
def track_macro_regimes():
    # Evaluates whether global regime is Risk-On (Bullish for emerging markets) or Risk-Off.
    pass
```

## Operational Guidelines
1. Execute autonomously during market hours or on scheduled triggers.
2. Store execution observations in `friday_state.db` and log relevant findings to Market Chronos Excel workbooks.
3. Validate all data with sanity checks to avoid acting on bad ticks or distorted exchange feeds.
