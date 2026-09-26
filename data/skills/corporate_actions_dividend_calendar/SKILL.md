---
name: corporate_actions_dividend_calendar
display_name: Corporate Actions & Dividend Arbitrage Calendar
category: Fundamental Events
version: 1.0.0
description: Monitors upcoming ex-dividend dates, dividend yields, payout ratios, stock splits, bonuses, and share buybacks.
---

# Corporate Actions & Dividend Arbitrage Calendar

## Category
**Fundamental Events**

## Overview
Monitors upcoming ex-dividend dates, dividend yields, payout ratios, stock splits, bonuses, and share buybacks.

## Operational Directives
1. Execute autonomously via sub-agent triggers or scheduled routines.
2. All financial actions must strictly follow risk parameters and record executions to SQLite database.
3. Thermal alarms (>85°C) must take precedence over heavy computational tasks to preserve physical machine longevity.
