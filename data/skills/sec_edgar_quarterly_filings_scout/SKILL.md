---
name: sec_edgar_quarterly_filings_scout
display_name: SEC EDGAR & Quarterly Filings Scout
category: Fundamental Analysis
version: 1.0.0
description: Automatically scrapes 10-Q (Quarterly) and 10-K (Annual) financial statements, balance sheets, and cash flows for US and Indian equities.
---

# SEC EDGAR & Quarterly Filings Scout

## Overview
Monitors company financial release dates, downloads published balance sheets, income statements, and cash flows, and parses them into standardized local JSON dossiers.

## Operational Logic
1. Track upcoming earnings release calendar for watchlist companies.
2. When statements are published, scrape Total Revenue, Net Income, Operating Cash Flow, Free Cash Flow, Total Debt, and Cash Reserves.
3. Save the dossier locally at `data/financial_filings/{SYMBOL}/{DATE}_financial_dossier.json`.
4. Expose the relative file path for correlation with intraday candlestick data in Market Chronos.
