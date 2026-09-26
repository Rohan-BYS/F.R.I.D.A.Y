---
name: paper_trading_simulator
display_name: Virtual Paper Trading & Backtesting Simulator
category: Quant Execution & Risk Simulation
version: 1.0.0
description: Simulates automated trade execution with ₹10 Lakh / $10,000 virtual balance, tracking trailing stops, win-rate %, and cumulative P&L in SQLite.
---

# Virtual Paper Trading & Backtesting Simulator

## Category
**Quant Execution & Risk Simulation**

## Overview
Simulates automated trade execution with ₹10 Lakh / $10,000 virtual balance, tracking trailing stops, win-rate %, and cumulative P&L in SQLite.

## Operational Directives
1. Execute autonomously via sub-agent triggers or scheduled routines.
2. All financial actions must strictly follow risk parameters and record executions to SQLite database.
3. Thermal alarms (>85°C) must take precedence over heavy computational tasks to preserve physical machine longevity.
