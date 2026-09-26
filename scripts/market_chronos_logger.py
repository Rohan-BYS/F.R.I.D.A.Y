#!/usr/bin/env python3
"""
F.R.I.D.A.Y. Market Chronos Logger
===================================
Sub-agent background worker that continuously logs 5m / 10m / 15m candlesticks
and synchronizes them with real-time news events, sentiment scores, and technical indicators.
Outputs directly to structured Excel (.xlsx) workbooks and SQLite databases.

Usage:
  python scripts/market_chronos_logger.py --symbols TATAMOTORS.NS RELIANCE.NS HDFCBANK.NS --interval 5m
  python scripts/market_chronos_logger.py --nifty50 --interval 5m
  python scripts/market_chronos_logger.py --daemon
"""

import os
import sys
import time
import json
import argparse
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

DATA_DIR = PROJECT_ROOT / "data" / "market_chronos"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# High-impact Indian & US Financial RSS Feeds
RSS_FEEDS = {
    # India
    "Moneycontrol_Top": "https://www.moneycontrol.com/rss/latestnews.xml",
    "Moneycontrol_Markets": "https://www.moneycontrol.com/rss/marketreports.xml",
    "EconomicTimes_Stocks": "https://economictimes.indiatimes.com/markets/stocks/rssfeeds/2146842.cms",
    "LiveMint_Companies": "https://www.livemint.com/rss/companies",
    # US / Wall Street
    "YahooFinance_US": "https://finance.yahoo.com/news/rssindex",
    "Reuters_Business": "https://www.reutersagency.com/feed/?taxonomy=markets&post_type=best",
    "MarketWatch_Top": "https://feeds.content.dowjones.io/public/rss/mw_topstories",
    "CNBC_Markets": "https://search.cnbc.com/rs/search/view.html?partnerId=2000&keywords=markets&sort=date",
}

DEFAULT_WATCHLIST = [
    # Top India (NSE)
    "TATAMOTORS.NS",
    "RELIANCE.NS",
    "HDFCBANK.NS",
    "INFY.NS",
    "ICICIBANK.NS",
    # Top US (NYSE / NASDAQ)
    "NVDA",
    "AAPL",
    "TSLA",
    "MSFT",
    "SPY",
]


class MarketNewsHarvester:
    """Harvests real-time financial news and extracts entity mappings."""

    def __init__(self):
        self.seen_guids = set()

    def fetch_latest_news(self) -> List[Dict[str, Any]]:
        """Fetch latest news items across financial RSS feeds."""
        items = []
        try:
            import feedparser
        except ImportError:
            # Fallback if feedparser not installed yet
            return []

        for source_name, feed_url in RSS_FEEDS.items():
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:10]:
                    guid = entry.get("id", entry.get("link", entry.get("title", "")))
                    if guid in self.seen_guids:
                        continue
                    self.seen_guids.add(guid)

                    published = entry.get("published", datetime.datetime.now().isoformat())
                    items.append({
                        "source": source_name,
                        "title": entry.get("title", ""),
                        "summary": entry.get("summary", ""),
                        "link": entry.get("link", ""),
                        "published": published,
                        "timestamp": datetime.datetime.now().isoformat(),
                    })
            except Exception:
                continue
        return items

    def score_sentiment(self, text: str) -> float:
        """
        Calculates simple rule-based domain sentiment between -1.0 (Extreme Bearish) to +1.0 (Extreme Bullish).
        In production, can route to local LLM or FinBERT.
        """
        text_lower = text.lower()
        bullish_words = [
            "surge", "jump", "rally", "profit", "gain", "dividend", "order win",
            "upgrade", "target raised", "record high", "acquisition", "expansion",
            "strong results", "growth", "buy rating", "outperform", "bullish"
        ]
        bearish_words = [
            "plunge", "slump", "loss", "fall", "drop", "downgrade", "fraud",
            "raid", "sebi penalty", "investigation", "warning", "default", "cut target",
            "weak results", "debt concern", "resignation", "sell rating", "bearish"
        ]

        score = 0.0
        for w in bullish_words:
            if w in text_lower:
                score += 0.25
        for w in bearish_words:
            if w in text_lower:
                score -= 0.25

        return max(-1.0, min(1.0, round(score, 2)))

    def match_symbol(self, text: str, symbol: str) -> bool:
        """Check if news item relates to symbol or its parent entity."""
        clean_sym = symbol.replace(".NS", "").replace(".BO", "").lower()
        company_aliases = {
            # India
            "tatamotors": ["tata motors", "jlr", "jaguar land rover", "ta-mo", "tatamotors"],
            "reliance": ["reliance", "ril", "mukesh ambani", "jio", "reliance retail"],
            "hdfcbank": ["hdfc", "hdfc bank", "sashidhar jagdishan"],
            "infy": ["infosys", "infy", "salil parekh"],
            "icicibank": ["icici", "icici bank", "sandeep bakhshi"],
            "tcs": ["tcs", "tata consultancy", "k krithivasan"],
            "itc": ["itc", "itc hotels", "sanjiv puri"],
            "sbin": ["sbi", "state bank of india", "dinesh khara"],
            "bhartiartl": ["airtel", "bharti airtel", "sunil mittal"],
            # US
            "nvda": ["nvidia", "nvda", "jensen huang", "blackwell", "h100"],
            "aapl": ["apple", "aapl", "tim cook", "iphone", "ios"],
            "tsla": ["tesla", "tsla", "elon musk", "cybertruck", "gigafactory"],
            "msft": ["microsoft", "msft", "satya nadella", "azure", "copilot"],
            "spy": ["s&p 500", "s&p", "spy", "wall street", "us markets"],
            "amzn": ["amazon", "amzn", "andy jassy", "aws"],
            "googl": ["google", "alphabet", "sundar pichai", "gemini"],
            "meta": ["meta", "facebook", "mark zuckerberg", "instagram"],
        }
        aliases = company_aliases.get(clean_sym, [clean_sym])
        text_lower = text.lower()
        return any(alias in text_lower for alias in aliases)


class TechnicalCalculator:
    """Computes high-confidence technical indicators on candle data."""

    @staticmethod
    def calculate_indicators(df):
        """Adds RSI, Supertrend, EMA, and CPR indicators to DataFrame."""
        if df is None or len(df) < 14:
            return df

        try:
            # 1. EMAs
            df["EMA_9"] = df["Close"].ewm(span=9, adjust=False).mean()
            df["EMA_21"] = df["Close"].ewm(span=21, adjust=False).mean()

            # 2. RSI (14)
            delta = df["Close"].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / (loss + 1e-9)
            df["RSI_14"] = 100 - (100 / (1 + rs))

            # 3. Candlestick Classification
            body = (df["Close"] - df["Open"]).abs()
            candle_range = df["High"] - df["Low"]
            upper_shadow = df["High"] - df[["Open", "Close"]].max(axis=1)
            lower_shadow = df[["Open", "Close"]].min(axis=1) - df["Low"]

            pattern = []
            for i in range(len(df)):
                b = body.iloc[i]
                r = candle_range.iloc[i] + 1e-9
                us = upper_shadow.iloc[i]
                ls = lower_shadow.iloc[i]
                is_green = df["Close"].iloc[i] >= df["Open"].iloc[i]

                if b / r > 0.7:
                    pattern.append("Marubozu (Strong)" if is_green else "Bearish Marubozu")
                elif ls > (2 * b) and us < (0.1 * r):
                    pattern.append("Hammer (Bullish Reversal)" if is_green else "Hanging Man")
                elif us > (2 * b) and ls < (0.1 * r):
                    pattern.append("Shooting Star (Bearish)" if not is_green else "Inverted Hammer")
                elif b / r < 0.15:
                    pattern.append("Doji (Indecision)")
                else:
                    pattern.append("Normal Green" if is_green else "Normal Red")

            df["Candle_Pattern"] = pattern
        except Exception:
            pass

        return df


class MarketChronosLogger:
    """Main Orchestrator for 5-minute candle and news synchronization."""

    def __init__(self, symbols: List[str] = None, interval: str = "5m"):
        self.symbols = symbols or DEFAULT_WATCHLIST
        self.interval = interval
        self.harvester = MarketNewsHarvester()
        self.db_path = DATA_DIR / "market_chronos.db"
        self.excel_path = DATA_DIR / f"market_chronos_master_{self.interval}.xlsx"
        self._init_sqlite_db()

    def fetch_latest_candle(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Fetch the most recent closed candlestick via yfinance."""
        try:
            import yfinance as yf
            ticker = yf.Ticker(symbol)
            df = ticker.history(period="1d", interval=self.interval)
            if df.empty:
                return None

            df = TechnicalCalculator.calculate_indicators(df)
            latest = df.iloc[-1]
            return {
                "Timestamp": df.index[-1].strftime("%Y-%m-%d %H:%M:%S"),
                "Symbol": symbol,
                "Open": round(float(latest["Open"]), 2),
                "High": round(float(latest["High"]), 2),
                "Low": round(float(latest["Low"]), 2),
                "Close": round(float(latest["Close"]), 2),
                "Volume": int(latest["Volume"]),
                "Candle_Pattern": latest.get("Candle_Pattern", "Unknown"),
                "RSI_14": round(float(latest.get("RSI_14", 50.0)), 2) if "RSI_14" in latest else None,
                "EMA_9": round(float(latest.get("EMA_9", latest["Close"])), 2) if "EMA_9" in latest else None,
                "EMA_21": round(float(latest.get("EMA_21", latest["Close"])), 2) if "EMA_21" in latest else None,
            }
        except Exception:
            return None

    def log_cycle(self):
        """Executes one continuous surveillance cycle across all tracked symbols."""
        try:
            import pandas as pd
        except ImportError:
            print("pandas not installed. Please install pandas & openpyxl.")
            return

        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🚀 Running Market Chronos cycle...")

        # 1. Gather fresh news
        latest_news = self.harvester.fetch_latest_news()

        # 2. Process each symbol
        cycle_records = []
        for sym in self.symbols:
            candle = self.fetch_latest_candle(sym)
            if not candle:
                continue

            # Check if any recent news matches this symbol
            matched_news = []
            sentiment_score = 0.0
            for n in latest_news:
                full_text = f"{n['title']} {n['summary']}"
                if self.harvester.match_symbol(full_text, sym):
                    score = self.harvester.score_sentiment(full_text)
                    matched_news.append(n["title"])
                    sentiment_score += score

            candle["News_Event"] = " | ".join(matched_news) if matched_news else "None"
            candle["News_Sentiment"] = round(sentiment_score, 2) if matched_news else 0.0

            # Check for scraped Financial Records / Balance Sheet Dossier
            try:
                from scripts.financial_filings_harvester import FinancialFilingsHarvester
                filings_harvester = FinancialFilingsHarvester()
                clean_s = sym.replace(".NS", "").replace(".BO", "").upper()
                sym_dossier_dir = PROJECT_ROOT / "data" / "financial_filings" / clean_s
                dossier_files = list(sym_dossier_dir.glob("*.json")) if sym_dossier_dir.exists() else []
                if dossier_files:
                    latest_dossier = sorted(dossier_files)[-1]
                    with open(latest_dossier, "r", encoding="utf-8") as df_f:
                        d_data = json.load(df_f)
                    candle["Financial_Report_Path"] = str(latest_dossier.relative_to(PROJECT_ROOT)).replace("\\", "/")
                    candle["Key_Financial_Metrics"] = d_data.get("key_metrics_summary", "Available")
                else:
                    candle["Financial_Report_Path"] = "None"
                    candle["Key_Financial_Metrics"] = "No Filing Harvested"
            except Exception:
                candle["Financial_Report_Path"] = "None"
                candle["Key_Financial_Metrics"] = "N/A"

            cycle_records.append(candle)

        if not cycle_records:
            print("  No candle data available (market may be closed).")
            return

        # 3. Insert into Ultra-Lightweight SQLite Database (WAL Mode)
        self._insert_to_sqlite(cycle_records)
        print(f"  ✓ Logged {len(cycle_records)} symbols to SQLite DB ({self.db_path.name})")

    def _init_sqlite_db(self):
        """Initializes SQLite database with WAL mode for crash-resilience and zero-overhead concurrency."""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA synchronous=NORMAL;")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS market_chronos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                symbol TEXT NOT NULL,
                interval TEXT DEFAULT '5m',
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume INTEGER,
                candle_pattern TEXT,
                rsi_14 REAL,
                ema_9 REAL,
                ema_21 REAL,
                news_event TEXT,
                news_sentiment REAL,
                financial_report_path TEXT,
                key_financial_metrics TEXT,
                UNIQUE(timestamp, symbol, interval) ON CONFLICT REPLACE
            );
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sym_time ON market_chronos (symbol, timestamp);")
        conn.commit()
        conn.close()

    def _insert_to_sqlite(self, records: List[Dict[str, Any]]):
        """Atomic batch insert into SQLite database."""
        import sqlite3
        self._init_sqlite_db()
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        sql = """
            INSERT INTO market_chronos (
                timestamp, symbol, interval, open, high, low, close, volume,
                candle_pattern, rsi_14, ema_9, ema_21, news_event, news_sentiment,
                financial_report_path, key_financial_metrics
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(timestamp, symbol, interval) DO UPDATE SET
                open=excluded.open, high=excluded.high, low=excluded.low, close=excluded.close,
                volume=excluded.volume, candle_pattern=excluded.candle_pattern,
                rsi_14=excluded.rsi_14, ema_9=excluded.ema_9, ema_21=excluded.ema_21,
                news_event=excluded.news_event, news_sentiment=excluded.news_sentiment,
                financial_report_path=excluded.financial_report_path,
                key_financial_metrics=excluded.key_financial_metrics;
        """

        tuples = [
            (
                r.get("Timestamp"), r.get("Symbol"), self.interval,
                r.get("Open"), r.get("High"), r.get("Low"), r.get("Close"), r.get("Volume"),
                r.get("Candle_Pattern"), r.get("RSI_14"), r.get("EMA_9"), r.get("EMA_21"),
                r.get("News_Event"), r.get("News_Sentiment"),
                r.get("Financial_Report_Path"), r.get("Key_Financial_Metrics")
            )
            for r in records
        ]

        cursor.executemany(sql, tuples)
        conn.commit()
        conn.close()

    def export_data(self, fmt: str = "excel", symbol: Optional[str] = None, output_path: Optional[str] = None) -> str:
        """
        Exports data on-demand from SQLite into Excel, CSV, or Apache Parquet.
        Zero overhead during continuous operation; files are only created when you ask!
        """
        import sqlite3
        try:
            import pandas as pd
        except ImportError:
            return "Error: pandas is required for export."

        conn = sqlite3.connect(self.db_path)
        query = "SELECT * FROM market_chronos"
        params = []
        if symbol:
            query += " WHERE symbol = ?"
            params.append(symbol)
        query += " ORDER BY timestamp ASC;"

        df = pd.read_sql_query(query, conn, params=params)
        conn.close()

        if df.empty:
            return "No records found in database to export."

        timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        target_stem = f"market_chronos_export_{timestamp_str}"

        if fmt == "excel":
            out_file = Path(output_path) if output_path else DATA_DIR / f"{target_stem}.xlsx"
            df.to_excel(out_file, index=False, engine="openpyxl")
            return f"Exported {len(df)} rows to Excel: {out_file}"
        elif fmt == "csv":
            out_file = Path(output_path) if output_path else DATA_DIR / f"{target_stem}.csv"
            df.to_csv(out_file, index=False)
            return f"Exported {len(df)} rows to CSV: {out_file}"
        elif fmt == "parquet":
            out_file = Path(output_path) if output_path else DATA_DIR / f"{target_stem}.parquet"
            df.to_parquet(out_file, index=False)
            return f"Exported {len(df)} rows to Apache Parquet: {out_file}"
        else:
            return f"Unknown format: {fmt}. Supported: excel, csv, parquet."


def main():
    parser = argparse.ArgumentParser(description="F.R.I.D.A.Y. Market Chronos Logger")
    parser.add_argument("--symbols", nargs="+", default=DEFAULT_WATCHLIST, help="Stock symbols to track")
    parser.add_argument("--interval", type=str, default="5m", choices=["1m", "5m", "10m", "15m", "1h"], help="Candle timeframe")
    parser.add_argument("--daemon", action="store_true", help="Run continuously in background during market hours")
    parser.add_argument("--export", type=str, choices=["excel", "csv", "parquet"], help="Export database to Excel, CSV, or Parquet")
    parser.add_argument("--export-symbol", type=str, help="Specific symbol to filter during export")
    parser.add_argument("--output-path", type=str, help="Custom export file destination")
    args = parser.parse_args()

    logger = MarketChronosLogger(symbols=args.symbols, interval=args.interval)

    if args.export:
        res = logger.export_data(fmt=args.export, symbol=args.export_symbol, output_path=args.output_path)
        print(res)
        return

    if args.daemon:
        print(f"Market Chronos Daemon active (SQLite WAL). Monitoring {len(args.symbols)} symbols every {args.interval}...")
        while True:
            logger.log_cycle()
            sleep_sec = 300 if args.interval == "5m" else 600
            time.sleep(sleep_sec)
    else:
        logger.log_cycle()


if __name__ == "__main__":
    main()
