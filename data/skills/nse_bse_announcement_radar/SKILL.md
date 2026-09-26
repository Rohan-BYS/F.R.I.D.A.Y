---
name: nse_bse_announcement_radar
display_name: NSE & BSE Corporate Announcement Radar
category: Regulatory & Corporate Surveillance
version: 1.0.0
description: Surveils official exchange filings for board meetings, dividends, mergers, bulk deals, insider trading (SAST), and promoter pledges.
---

# NSE & BSE Corporate Announcement Radar

## Overview
Surveils official exchange filings for board meetings, dividends, mergers, bulk deals, insider trading (SAST), and promoter pledges.

## Category
**Regulatory & Corporate Surveillance**

## Architecture & Logic
```python
def check_exchange_filings(symbol, hours_lookback=24):
    # Queries NSE/BSE corporate disclosure APIs.
    # Extracts material events: Order wins, Capex announcements, SEBI inquiry clarifications.
    pass
```

## Operational Guidelines
1. Execute autonomously during market hours or on scheduled triggers.
2. Store execution observations in `friday_state.db` and log relevant findings to Market Chronos Excel workbooks.
3. Validate all data with sanity checks to avoid acting on bad ticks or distorted exchange feeds.
