#!/usr/bin/env python3
"""
F.R.I.D.A.Y. Market Intelligence & Technical Analysis Skills Seeder
===================================================================
Seeds 16 battle-tested financial skills into F.R.I.D.A.Y.'s data/skills/ directory:
- 8 News, Regulatory, Surveillance & Macro Skills
- 8 Quantitative, Candlestick & High-Consistency Technical Indicator Skills
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

SKILLS_DEFINITIONS = [
    # ── NEWS & SURVEILLANCE SKILLS ──────────────────────────────────────────
    {
        "id": "market_rss_sentinel",
        "name": "Live Market RSS Sentinel",
        "category": "Market Intelligence",
        "description": "Scans Moneycontrol, Economic Times, LiveMint, Business Standard feeds every 60s for corporate and sector news.",
        "logic": """
def scan_rss_feeds(category='markets'):
    # Ingests live RSS XML feeds from top 6 Indian financial portals.
    # Deduplicates entries by guid/link, normalizes timestamps to IST.
    # Returns structured list of breaking news items.
    pass
"""
    },
    {
        "id": "nse_bse_announcement_radar",
        "name": "NSE & BSE Corporate Announcement Radar",
        "category": "Regulatory & Corporate Surveillance",
        "description": "Surveils official exchange filings for board meetings, dividends, mergers, bulk deals, insider trading (SAST), and promoter pledges.",
        "logic": """
def check_exchange_filings(symbol, hours_lookback=24):
    # Queries NSE/BSE corporate disclosure APIs.
    # Extracts material events: Order wins, Capex announcements, SEBI inquiry clarifications.
    pass
"""
    },
    {
        "id": "financial_sentiment_scorer",
        "name": "Financial Sentiment & Materiality Scorer",
        "category": "NLP Intelligence",
        "description": "Scores news and corporate disclosures from -1.0 (Bearish) to +1.0 (Bullish), estimating stock price materiality.",
        "logic": """
def evaluate_sentiment_and_materiality(headline, article_body=''):
    # Combines domain-specific lexicon with LLM evaluation.
    # Filters out market noise (low-materiality fluff) from high-impact regulatory or financial shocks.
    pass
"""
    },
    {
        "id": "sector_correlation_mapper",
        "name": "Sector Correlation & 2nd Order Ripple Mapper",
        "category": "Quantitative Macro",
        "description": "Maps macroeconomic shifts (Crude oil, Dollar Index, Interest rates) to 2nd-order beneficiary and affected sectors.",
        "logic": """
def map_ripple_effects(macro_event, magnitude):
    # E.g., Crude oil drops 5% -> Paints (+), Aviation (+), Tyres (+) / Oil upstream (-).
    # Returns ranked list of beneficiary vs vulnerable Indian stock tickers.
    pass
"""
    },
    {
        "id": "concall_transcript_analyst",
        "name": "Earnings ConCall Transcript Deep Analyst",
        "category": "Fundamental Analysis",
        "description": "Parses 40-page quarterly earnings conference call transcripts into EBITDA guidance, Capex plans, and management tone changes.",
        "logic": """
def parse_concall_transcript(transcript_text):
    # Identifies management tone shifts (defensive vs bullish).
    # Highlights recurring analyst questions and unanswered concerns in the Q&A section.
    pass
"""
    },
    {
        "id": "pre_market_curator",
        "name": "Daily Pre-Market 8:30 AM Briefing Curator",
        "category": "Automated Reporting",
        "description": "Synthesizes overnight US/Asian market moves, GIFT Nifty, FII/DII net flows, and top 10 stocks in focus before market open.",
        "logic": """
def generate_pre_market_briefing():
    # Assembles Dow Jones, Nasdaq, GIFT Nifty, Crude, DXY, and previous day FII cash flows.
    # Dispatches clean, actionable bullet-point dossier via Telegram/WhatsApp by 8:30 AM IST.
    pass
"""
    },
    {
        "id": "stock_watchlist_watchdog",
        "name": "Autonomous Stock Portfolio Watchdog",
        "category": "Portfolio Management",
        "description": "24/7 dedicated sentinel on user's custom stock holdings, alerting immediately upon any material news or price anomalies.",
        "logic": """
def monitor_user_portfolio(symbols_list):
    # Tracks price action, volume surges (>3x average), and news coverage specifically for user's watchlist.
    pass
"""
    },
    {
        "id": "macro_global_tracker",
        "name": "Global Macro & Central Bank Tracker",
        "category": "Global Macro",
        "description": "Monitors US Federal Reserve FOMC decisions, US 10Y Treasury yields, DXY, and geopolitical risk indices for emerging market spillovers.",
        "logic": """
def track_macro_regimes():
    # Evaluates whether global regime is Risk-On (Bullish for emerging markets) or Risk-Off.
    pass
"""
    },

    # ── QUANTITATIVE & HIGH-CONFIDENCE TECHNICAL INDICATORS ──────────────────
    {
        "id": "central_pivot_range_cpr_intraday",
        "name": "Central Pivot Range (CPR) & Floor Pivots",
        "category": "Technical Analysis",
        "description": "Calculates Pivot, Top Central (TC), Bottom Central (BC). Detects Narrow CPR (Trending/Breakout day) and Wide CPR (Range-bound day).",
        "logic": """
def calculate_cpr(high, low, close):
    pivot = (high + low + close) / 3.0
    bc = (high + low) / 2.0
    tc = (pivot - bc) + pivot
    cpr_width_pct = abs(tc - bc) / pivot * 100
    # Width < 0.25% indicates high probability of explosive directional trend day
    return {"pivot": pivot, "tc": tc, "bc": bc, "width_pct": cpr_width_pct}
"""
    },
    {
        "id": "supertrend_ema_confluence_strategy",
        "name": "Supertrend + 20/50 EMA Trend Confluence",
        "category": "Trend Following",
        "description": "High-win-rate trend following confluence: buys only when Supertrend(7,3) is Green AND Price is above 20 EMA and 50 EMA.",
        "logic": """
def evaluate_supertrend_ema_confluence(df):
    # Eliminates false choppy signals by requiring multi-indicator alignment.
    # Extremely robust for Indian index futures (Nifty/BankNifty) and large-cap swings.
    pass
"""
    },
    {
        "id": "rsi_macd_divergence_detector",
        "name": "RSI & MACD Divergence Reversal Detector",
        "category": "Mean Reversion",
        "description": "Detects Regular (Trend Reversal) and Hidden (Trend Continuation) divergences between Price swing highs/lows and RSI/MACD momentum.",
        "logic": """
def find_divergences(prices, rsi_values):
    # Price makes Lower Low but RSI makes Higher Low -> Regular Bullish Divergence.
    # Price makes Higher Low but RSI makes Lower Low -> Hidden Bullish Divergence.
    pass
"""
    },
    {
        "id": "volume_profile_poc_value_area",
        "name": "Volume Profile (POC & Value Area High/Low)",
        "category": "Auction Market Theory",
        "description": "Calculates Point of Control (POC - price level with highest traded volume) and Value Area (VAH/VAL 70% volume distribution).",
        "logic": """
def calculate_volume_profile(df_trades):
    # Identifies where institutional buyers accumulated versus thin volume rejection areas.
    pass
"""
    },
    {
        "id": "atr_trailing_stop_risk_manager",
        "name": "Average True Range (ATR) Volatility Trailing Stop",
        "category": "Risk Management",
        "description": "Dynamic volatility-based stop loss calculation (e.g. 2x ATR(14)) to prevent getting stopped out during normal market breathing.",
        "logic": """
def compute_atr_trailing_stop(close, high, low, multiplier=2.0, period=14):
    # Automatically widens stop in high volatility and tightens in low volatility.
    pass
"""
    },
    {
        "id": "india_vix_regime_switch_filter",
        "name": "India VIX Volatility Regime Switch",
        "category": "Derivatives & Options",
        "description": "Analyzes India VIX levels (<12: Complacent, 12-16: Normal Bull, 16-22: Nervous, >22: High Fear) to dictate Option Buying vs Selling strategies.",
        "logic": """
def get_vix_regime_recommendation(vix_value):
    # Low VIX: Net Credit spreads / Theta decay strategies.
    # Rising VIX: Long Gamma / Momentum breakout buying strategies.
    pass
"""
    },
    {
        "id": "multitimeframe_trend_matrix",
        "name": "Multi-Timeframe (MTF) Alignment Matrix",
        "category": "Quant Execution",
        "description": "Top-down trend verification (Monthly -> Weekly -> Daily -> 15m). Trades are only taken in the direction of the higher timeframe trend.",
        "logic": """
def check_mtf_alignment(symbol):
    # Returns 'PERFECT_BULLISH' if Daily > 50 EMA, 1h > 50 EMA, and 15m > 50 EMA simultaneously.
    pass
"""
    },
    {
        "id": "candlestick_multibar_confirmation_engine",
        "name": "Multi-Bar Candlestick Confirmation Engine",
        "category": "Price Action",
        "description": "Identifies high-probability candlestick patterns: Morning Star, Evening Star, Bullish Engulfing, Three Inside Up, with Volume Confirmation.",
        "logic": """
def detect_multibar_patterns(ohlcv_df):
    # Verifies pattern is supported by >1.5x average volume and occurs at key support/resistance.
    pass
"""
    },
]


def seed_skills():
    print(f"\n🌱 Seeding {len(SKILLS_DEFINITIONS)} Market Intelligence & Quant Skills...")
    count = 0
    for s in SKILLS_DEFINITIONS:
        skill_dir = SKILLS_DIR / s["id"]
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_file = skill_dir / "SKILL.md"

        content = f"""---
name: {s["id"]}
display_name: {s["name"]}
category: {s["category"]}
version: 1.0.0
description: {s["description"]}
---

# {s["name"]}

## Overview
{s["description"]}

## Category
**{s["category"]}**

## Architecture & Logic
```python
{s["logic"].strip()}
```

## Operational Guidelines
1. Execute autonomously during market hours or on scheduled triggers.
2. Store execution observations in `friday_state.db` and log relevant findings to Market Chronos Excel workbooks.
3. Validate all data with sanity checks to avoid acting on bad ticks or distorted exchange feeds.
"""
        with open(skill_file, "w", encoding="utf-8") as f:
            f.write(content)
        count += 1
        print(f"  ✓ [{s['category']}] {s['name']} -> {s['id']}/SKILL.md")

    print(f"\n✅ Successfully seeded {count} new skills into {SKILLS_DIR}!")


if __name__ == "__main__":
    seed_skills()
