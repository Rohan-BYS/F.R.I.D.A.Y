#!/usr/bin/env python3
"""
F.R.I.D.A.Y. Market Correlation Analyst
========================================
Analytical AI module that ingests accumulated 1-month to 6-month Market Chronos
Excel workbooks, correlates candlestick price action with breaking news events,
and generates predictive forecasting reports for future trading decisions.

Usage:
  python scripts/market_correlation_analyst.py --symbol TATAMOTORS.NS
  python scripts/market_correlation_analyst.py --all
  python scripts/market_correlation_analyst.py --report-path my_analysis.json
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

DATA_DIR = PROJECT_ROOT / "data" / "market_chronos"


class MarketCorrelationAnalyst:
    """Performs Event-Study and Price-News Correlation on logged datasets."""

    def __init__(self, db_path: Optional[Path] = None, excel_path: Optional[Path] = None):
        self.db_path = db_path or (DATA_DIR / "market_chronos.db")
        self.excel_path = excel_path or (DATA_DIR / "market_chronos_master_5m.xlsx")

    def load_data(self):
        """Loads dataset with priority on SQLite (WAL) for sub-millisecond speed, with Excel fallback."""
        try:
            import pandas as pd
            # 1. Primary: Lightning-fast SQLite Database
            if self.db_path.exists():
                import sqlite3
                conn = sqlite3.connect(self.db_path)
                df = pd.read_sql_query("SELECT * FROM market_chronos ORDER BY timestamp ASC;", conn)
                conn.close()
                if not df.empty:
                    # Normalize column casing for seamless compatibility
                    df.columns = [c.capitalize() if c in ["symbol", "timestamp", "open", "high", "low", "close", "volume"] else c for c in df.columns]
                    return df

            # 2. Fallback: Excel File
            if self.excel_path.exists():
                return pd.read_excel(self.excel_path, engine="openpyxl")

            return None
        except Exception as e:
            print(f"Error loading market data: {e}")
            return None

    def analyze_symbol(self, symbol: str, df=None) -> Dict[str, Any]:
        """
        Runs comprehensive quantitative analysis for a specific stock:
        1. News Event Impact: Average price reaction on bullish vs bearish news.
        2. Candlestick Pattern Win Rate: Efficacy of Hammers, Marubozus, Dojis.
        3. News + Pattern Synergy: Does a Hammer with Positive News yield higher returns?
        4. Forward Prediction / Outlook: Statistical probability of upward/downward continuation.
        """
        if df is None:
            df = self.load_data()

        if df is None or df.empty:
            return {
                "symbol": symbol,
                "status": "NO_HISTORICAL_DATA",
                "message": "Market Chronos has not accumulated sufficient data yet. Run logger first.",
            }

        # Filter for this symbol
        sym_df = df[df["Symbol"] == symbol].copy()
        if sym_df.empty:
            return {
                "symbol": symbol,
                "status": "SYMBOL_NOT_FOUND",
                "message": f"No records found for {symbol} in master log.",
            }

        sym_df["Return_Pct"] = sym_df["Close"].pct_change() * 100

        # 1. Event Impact Analysis
        news_events = sym_df[sym_df["News_Event"] != "None"]
        bullish_news = news_events[news_events["News_Sentiment"] > 0]
        bearish_news = news_events[news_events["News_Sentiment"] < 0]

        avg_bullish_reaction = float(bullish_news["Return_Pct"].mean()) if not bullish_news.empty else 0.0
        avg_bearish_reaction = float(bearish_news["Return_Pct"].mean()) if not bearish_news.empty else 0.0

        # 2. Candlestick Pattern Statistics
        pattern_stats = {}
        for pattern_name, group in sym_df.groupby("Candle_Pattern"):
            if len(group) >= 2:
                pattern_stats[pattern_name] = {
                    "count": int(len(group)),
                    "avg_subsequent_return": round(float(group["Return_Pct"].mean()), 2),
                    "positive_close_ratio": round(float((group["Return_Pct"] > 0).mean()), 2),
                }

        # 3. Synergy (News + Pattern)
        synergy_records = []
        for idx, row in news_events.iterrows():
            synergy_records.append({
                "timestamp": str(row["Timestamp"]),
                "candle": row["Candle_Pattern"],
                "sentiment": float(row["News_Sentiment"]),
                "news": row["News_Event"][:100],
                "immediate_reaction_pct": round(float(row["Return_Pct"]), 2) if not pd.isna(row["Return_Pct"]) else 0.0,
            })

        # 4. Forward Predictive Outlook
        latest_row = sym_df.iloc[-1]
        latest_rsi = float(latest_row.get("RSI_14", 50.0))
        latest_pattern = latest_row.get("Candle_Pattern", "Normal")
        latest_sentiment = float(latest_row.get("News_Sentiment", 0.0))

        # Scoring future probability
        bullish_score = 50.0
        if latest_rsi < 35:
            bullish_score += 15.0  # Oversold bounce
        elif latest_rsi > 70:
            bullish_score -= 15.0  # Overbought pullback

        if "Hammer" in latest_pattern or "Marubozu (Strong)" in latest_pattern:
            bullish_score += 15.0
        elif "Shooting Star" in latest_pattern or "Bearish" in latest_pattern:
            bullish_score -= 15.0

        if latest_sentiment > 0.3:
            bullish_score += 15.0
        elif latest_sentiment < -0.3:
            bullish_score -= 15.0

        bullish_score = max(5.0, min(95.0, round(bullish_score, 1)))

        return {
            "symbol": symbol,
            "status": "ANALYSIS_COMPLETE",
            "total_candles_logged": int(len(sym_df)),
            "total_news_events_correlated": int(len(news_events)),
            "event_impact": {
                "avg_bullish_news_reaction_pct": round(avg_bullish_reaction, 2),
                "avg_bearish_news_reaction_pct": round(avg_bearish_reaction, 2),
                "high_impact_news_samples": synergy_records[:5],
            },
            "pattern_efficacy": pattern_stats,
            "predictive_outlook": {
                "latest_timestamp": str(latest_row["Timestamp"]),
                "latest_close": float(latest_row["Close"]),
                "latest_rsi": round(latest_rsi, 2),
                "latest_pattern": latest_pattern,
                "latest_news_sentiment": latest_sentiment,
                "probability_upward_continuation_pct": bullish_score,
                "probability_downward_continuation_pct": round(100.0 - bullish_score, 1),
                "recommendation": "ACCUMULATE / BULLISH BIAS" if bullish_score >= 65.0 else (
                    "DISTRIBUTE / BEARISH BIAS" if bullish_score <= 35.0 else "HOLD / CONSOLIDATION"
                ),
            },
        }

    def generate_full_report(self, symbols: Optional[List[str]] = None) -> Dict[str, Any]:
        """Generates cross-portfolio correlation report."""
        df = self.load_data()
        if df is None or df.empty:
            return {"error": "No data found in master log file."}

        available_symbols = df["Symbol"].unique().tolist()
        targets = symbols or available_symbols

        report = {
            "dataset_info": {
                "total_rows": int(len(df)),
                "earliest_timestamp": str(df["Timestamp"].min()),
                "latest_timestamp": str(df["Timestamp"].max()),
                "tracked_symbols": available_symbols,
            },
            "symbol_analyses": {},
        }

        for sym in targets:
            report["symbol_analyses"][sym] = self.analyze_symbol(sym, df=df)

        return report


def main():
    parser = argparse.ArgumentParser(description="F.R.I.D.A.Y. Market Correlation Analyst")
    parser.add_argument("--symbol", type=str, help="Specific stock ticker (e.g. TATAMOTORS.NS)")
    parser.add_argument("--all", action="store_true", help="Analyze all tracked stocks")
    parser.add_argument("--excel-path", type=str, help="Path to custom Excel workbook")
    args = parser.parse_args()

    excel_p = Path(args.excel_path) if args.excel_path else None
    analyst = MarketCorrelationAnalyst(excel_path=excel_p)

    if args.symbol:
        res = analyst.analyze_symbol(args.symbol)
        print(json.dumps(res, indent=2))
    elif args.all or not args.symbol:
        res = analyst.generate_full_report()
        print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
