#!/usr/bin/env python3
"""
F.R.I.D.A.Y. Corporate Actions & Dividend Calendar
===================================================
Tracks upcoming ex-dividend dates, dividend yield payouts, stock splits,
and corporate share buybacks for US and Indian equities.

Usage:
  python scripts/corporate_actions_calendar.py --symbol AAPL
  python scripts/corporate_actions_calendar.py --symbol TATAMOTORS.NS
"""

import os
import sys
import json
import argparse
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

ACTIONS_DIR = PROJECT_ROOT / "data" / "corporate_actions"
ACTIONS_DIR.mkdir(parents=True, exist_ok=True)


class CorporateActionsCalendar:
    """Tracks and schedules corporate actions (Dividends, Splits, Buybacks)."""

    def __init__(self, storage_dir: Optional[Path] = None):
        self.storage_dir = storage_dir or ACTIONS_DIR

    def get_corporate_actions(self, symbol: str) -> Dict[str, Any]:
        """Fetches dividends and splits history + next corporate dates."""
        try:
            import yfinance as yf
            ticker = yf.Ticker(symbol)

            # Dividends & Splits
            divs = ticker.dividends
            splits = ticker.splits
            info = getattr(ticker, "info", {}) or {}

            recent_dividends = []
            if not divs.empty:
                for date, val in divs.tail(5).items():
                    date_str = date.strftime("%Y-%m-%d") if hasattr(date, "strftime") else str(date)[:10]
                    recent_dividends.append({"date": date_str, "amount": round(float(val), 2)})

            recent_splits = []
            if not splits.empty:
                for date, val in splits.tail(3).items():
                    date_str = date.strftime("%Y-%m-%d") if hasattr(date, "strftime") else str(date)[:10]
                    recent_splits.append({"date": date_str, "split_ratio": float(val)})

            ex_div_timestamp = info.get("exDividendDate")
            ex_div_date = datetime.datetime.fromtimestamp(ex_div_timestamp).strftime("%Y-%m-%d") if ex_div_timestamp else "None Scheduled"

            result = {
                "symbol": symbol,
                "current_dividend_yield": f"{round(info.get('dividendYield', 0.0) * 100, 2)}%" if info.get('dividendYield') else "0.0%",
                "payout_ratio": f"{round(info.get('payoutRatio', 0.0) * 100, 2)}%" if info.get('payoutRatio') else "N/A",
                "upcoming_ex_dividend_date": ex_div_date,
                "dividend_rate_annual": info.get("dividendRate", 0.0),
                "recent_dividends": recent_dividends,
                "recent_splits": recent_splits,
                "updated_at": datetime.datetime.now().isoformat(),
            }

            # Save report
            clean_sym = symbol.replace(".", "_")
            out_file = self.storage_dir / f"{clean_sym}_actions.json"
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2)

            result["file_path"] = str(out_file.relative_to(PROJECT_ROOT)).replace("\\", "/")
            return result

        except Exception as e:
            return {"status": "ERROR", "symbol": symbol, "message": str(e)}


def main():
    parser = argparse.ArgumentParser(description="F.R.I.D.A.Y. Corporate Actions Calendar")
    parser.add_argument("--symbol", type=str, default="AAPL", help="Ticker symbol (e.g. AAPL, INFY.NS)")
    args = parser.parse_args()

    cal = CorporateActionsCalendar()
    res = cal.get_corporate_actions(args.symbol)
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
