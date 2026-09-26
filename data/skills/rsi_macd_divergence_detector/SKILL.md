---
name: rsi_macd_divergence_detector
display_name: RSI & MACD Divergence Reversal Detector
category: Mean Reversion
version: 1.0.0
description: Detects Regular (Trend Reversal) and Hidden (Trend Continuation) divergences between Price swing highs/lows and RSI/MACD momentum.
---

# RSI & MACD Divergence Reversal Detector

## Overview
Detects Regular (Trend Reversal) and Hidden (Trend Continuation) divergences between Price swing highs/lows and RSI/MACD momentum.

## Category
**Mean Reversion**

## Architecture & Logic
```python
def find_divergences(prices, rsi_values):
    # Price makes Lower Low but RSI makes Higher Low -> Regular Bullish Divergence.
    # Price makes Higher Low but RSI makes Lower Low -> Hidden Bullish Divergence.
    pass
```

## Operational Guidelines
1. Execute autonomously during market hours or on scheduled triggers.
2. Store execution observations in `friday_state.db` and log relevant findings to Market Chronos Excel workbooks.
3. Validate all data with sanity checks to avoid acting on bad ticks or distorted exchange feeds.
