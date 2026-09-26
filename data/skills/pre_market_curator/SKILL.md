---
name: pre_market_curator
display_name: Daily Pre-Market 8:30 AM Briefing Curator
category: Automated Reporting
version: 1.0.0
description: Synthesizes overnight US/Asian market moves, GIFT Nifty, FII/DII net flows, and top 10 stocks in focus before market open.
---

# Daily Pre-Market 8:30 AM Briefing Curator

## Overview
Synthesizes overnight US/Asian market moves, GIFT Nifty, FII/DII net flows, and top 10 stocks in focus before market open.

## Category
**Automated Reporting**

## Architecture & Logic
```python
def generate_pre_market_briefing():
    # Assembles Dow Jones, Nasdaq, GIFT Nifty, Crude, DXY, and previous day FII cash flows.
    # Dispatches clean, actionable bullet-point dossier via Telegram/WhatsApp by 8:30 AM IST.
    pass
```

## Operational Guidelines
1. Execute autonomously during market hours or on scheduled triggers.
2. Store execution observations in `friday_state.db` and log relevant findings to Market Chronos Excel workbooks.
3. Validate all data with sanity checks to avoid acting on bad ticks or distorted exchange feeds.
