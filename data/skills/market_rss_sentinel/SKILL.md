---
name: market_rss_sentinel
display_name: Live Market RSS Sentinel
category: Market Intelligence
version: 1.0.0
description: Scans Moneycontrol, Economic Times, LiveMint, Business Standard feeds every 60s for corporate and sector news.
---

# Live Market RSS Sentinel

## Overview
Scans Moneycontrol, Economic Times, LiveMint, Business Standard feeds every 60s for corporate and sector news.

## Category
**Market Intelligence**

## Architecture & Logic
```python
def scan_rss_feeds(category='markets'):
    # Ingests live RSS XML feeds from top 6 Indian financial portals.
    # Deduplicates entries by guid/link, normalizes timestamps to IST.
    # Returns structured list of breaking news items.
    pass
```

## Operational Guidelines
1. Execute autonomously during market hours or on scheduled triggers.
2. Store execution observations in `friday_state.db` and log relevant findings to Market Chronos Excel workbooks.
3. Validate all data with sanity checks to avoid acting on bad ticks or distorted exchange feeds.
