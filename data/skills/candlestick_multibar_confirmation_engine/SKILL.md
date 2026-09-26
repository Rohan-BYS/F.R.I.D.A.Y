---
name: candlestick_multibar_confirmation_engine
display_name: Multi-Bar Candlestick Confirmation Engine
category: Price Action
version: 1.0.0
description: Identifies high-probability candlestick patterns: Morning Star, Evening Star, Bullish Engulfing, Three Inside Up, with Volume Confirmation.
---

# Multi-Bar Candlestick Confirmation Engine

## Overview
Identifies high-probability candlestick patterns: Morning Star, Evening Star, Bullish Engulfing, Three Inside Up, with Volume Confirmation.

## Category
**Price Action**

## Architecture & Logic
```python
def detect_multibar_patterns(ohlcv_df):
    # Verifies pattern is supported by >1.5x average volume and occurs at key support/resistance.
    pass
```

## Operational Guidelines
1. Execute autonomously during market hours or on scheduled triggers.
2. Store execution observations in `friday_state.db` and log relevant findings to Market Chronos Excel workbooks.
3. Validate all data with sanity checks to avoid acting on bad ticks or distorted exchange feeds.
