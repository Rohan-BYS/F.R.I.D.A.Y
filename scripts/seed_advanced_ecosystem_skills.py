#!/usr/bin/env python3
"""
F.R.I.D.A.Y. Advanced Ecosystem Skills Seeder
=============================================
Seeds 7 new advanced ecosystem skills into data/skills/:
1. paper_trading_simulator
2. whale_super_investor_tracker
3. options_max_pain_radar
4. visual_candlestick_plotter
5. corporate_actions_dividend_calendar
6. social_buzz_sentiment_sentinel
7. hardware_thermal_sentinel
"""

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = PROJECT_ROOT / "data" / "skills"
SKILLS_DIR.mkdir(parents=True, exist_ok=True)

if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SKILLS = [
    {
        "id": "paper_trading_simulator",
        "name": "Virtual Paper Trading & Backtesting Simulator",
        "category": "Quant Execution & Risk Simulation",
        "description": "Simulates automated trade execution with ₹10 Lakh / $10,000 virtual balance, tracking trailing stops, win-rate %, and cumulative P&L in SQLite.",
    },
    {
        "id": "whale_super_investor_tracker",
        "name": "Whale & Super-Investor Portfolio Tracker",
        "category": "Institutional Intelligence",
        "description": "Tracks portfolio holdings and bulk deals of Indian super-investors (Kedia, Kacholia, Damani) and US SEC 13F hedge fund managers (Buffett, Burry).",
    },
    {
        "id": "options_max_pain_radar",
        "name": "Options Chain & Max Pain Radar",
        "category": "Derivatives & Options",
        "description": "Calculates Put-Call Ratio (PCR), Call/Put Open Interest concentration walls, and solves for the Max Pain expiry pin price.",
    },
    {
        "id": "visual_candlestick_plotter",
        "name": "Automated Visual Candlestick & Indicator Plotter",
        "category": "Visual Analytics",
        "description": "Renders high-resolution dark-mode candlestick charts (PNG) with 9/21 EMA overlays and RSI subplots, ready for Telegram or Desktop HUD.",
    },
    {
        "id": "corporate_actions_dividend_calendar",
        "name": "Corporate Actions & Dividend Arbitrage Calendar",
        "category": "Fundamental Events",
        "description": "Monitors upcoming ex-dividend dates, dividend yields, payout ratios, stock splits, bonuses, and share buybacks.",
    },
    {
        "id": "social_buzz_sentiment_sentinel",
        "name": "Social Buzz & FinTwit Pulse Sentinel",
        "category": "Alternative Data",
        "description": "Tracks cashtag mention momentum, social buzz velocity, and retail FOMO risk to catch breakout trends before traditional media.",
    },
    {
        "id": "hardware_thermal_sentinel",
        "name": "Hardware & Thermal Overheat Sentinel",
        "category": "Host Security & Maintenance",
        "description": "Continuously checks CPU/GPU temperatures, disk storage, and RAM usage on physical host machine, auto-throttling on thermal spikes >85°C.",
    },
]


def seed():
    print(f"\n🌱 Seeding {len(SKILLS)} Advanced Ecosystem Skills...")
    for s in SKILLS:
        s_dir = SKILLS_DIR / s["id"]
        s_dir.mkdir(parents=True, exist_ok=True)
        s_file = s_dir / "SKILL.md"

        content = f"""---
name: {s["id"]}
display_name: {s["name"]}
category: {s["category"]}
version: 1.0.0
description: {s["description"]}
---

# {s["name"]}

## Category
**{s["category"]}**

## Overview
{s["description"]}

## Operational Directives
1. Execute autonomously via sub-agent triggers or scheduled routines.
2. All financial actions must strictly follow risk parameters and record executions to SQLite database.
3. Thermal alarms (>85°C) must take precedence over heavy computational tasks to preserve physical machine longevity.
"""
        with open(s_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✓ [{s['category']}] {s['name']} -> {s['id']}/SKILL.md")

    print(f"\n✅ All {len(SKILLS)} advanced ecosystem skills successfully seeded into {SKILLS_DIR}!")


if __name__ == "__main__":
    seed()
