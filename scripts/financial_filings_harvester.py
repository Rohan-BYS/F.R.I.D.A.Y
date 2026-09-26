#!/usr/bin/env python3
"""
F.R.I.D.A.Y. Financial Filings & Balance Sheet Harvester
========================================================
Autonomous module that tracks earnings release dates, scrapes balance sheets,
income statements, and cash flows for US (SEC 10-Q/10-K) and Indian (Quarterly/Annual)
stocks, saves structured dossiers locally, and returns local file paths for Excel linking.

Usage:
  python scripts/financial_filings_harvester.py --symbol NVDA
  python scripts/financial_filings_harvester.py --symbol TATAMOTORS.NS
  python scripts/financial_filings_harvester.py --sync-watchlist
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

FILINGS_DIR = PROJECT_ROOT / "data" / "financial_filings"
FILINGS_DIR.mkdir(parents=True, exist_ok=True)


class FinancialFilingsHarvester:
    """Scrapes, normalizes, and stores corporate balance sheets and quarterly reports."""

    def __init__(self, storage_dir: Optional[Path] = None):
        self.storage_dir = storage_dir or FILINGS_DIR

    def get_upcoming_earnings_date(self, symbol: str) -> Optional[str]:
        """Fetches next scheduled earnings/financial release date."""
        try:
            import yfinance as yf
            ticker = yf.Ticker(symbol)
            cal = ticker.calendar
            if cal is not None and not cal.empty if hasattr(cal, 'empty') else cal:
                if isinstance(cal, dict) and "Earnings Date" in cal:
                    dates = cal["Earnings Date"]
                    return str(dates[0]) if dates else None
                elif hasattr(cal, "T") and "Earnings Date" in cal.T.columns:
                    return str(cal.T["Earnings Date"].iloc[0])
            return None
        except Exception:
            return None

    def harvest_financial_dossier(self, symbol: str) -> Dict[str, Any]:
        """
        Extracts the latest Balance Sheet, Income Statement, and Cash Flow.
        Saves locally as a structured JSON dossier and returns metadata + local path.
        """
        clean_sym = symbol.replace(".NS", "").replace(".BO", "").upper()
        sym_dir = self.storage_dir / clean_sym
        sym_dir.mkdir(parents=True, exist_ok=True)

        try:
            import yfinance as yf
            ticker = yf.Ticker(symbol)

            # 1. Fetch statements
            q_fin = ticker.quarterly_financials
            q_bs = ticker.quarterly_balance_sheet
            q_cf = ticker.quarterly_cashflow

            if q_fin is None or q_fin.empty:
                return {
                    "symbol": symbol,
                    "status": "NO_ONLINE_FINANCIALS_FOUND",
                    "file_path": None,
                    "metrics_summary": "N/A",
                }

            latest_date_col = q_fin.columns[0]
            date_str = latest_date_col.strftime("%Y-%m-%d") if hasattr(latest_date_col, 'strftime') else str(latest_date_col)[:10]

            # 2. Extract Key Financial Metrics
            def get_val(df, row_name):
                if df is not None and not df.empty and row_name in df.index:
                    val = df.loc[row_name].iloc[0]
                    if val is not None and not (hasattr(val, '__iter__') and not isinstance(val, str)):
                        try:
                            num = float(val)
                            if abs(num) >= 1e9:
                                return f"${round(num / 1e9, 2)}B"
                            elif abs(num) >= 1e6:
                                return f"${round(num / 1e6, 2)}M"
                            return str(round(num, 2))
                        except (ValueError, TypeError):
                            return str(val)
                return "N/A"

            revenue = get_val(q_fin, "Total Revenue") or get_val(q_fin, "Operating Revenue")
            net_income = get_val(q_fin, "Net Income") or get_val(q_fin, "Net Income Common Stockholders")
            operating_cash_flow = get_val(q_cf, "Operating Cash Flow") or get_val(q_cf, "Cash Flow From Continuing Operating Activities")
            free_cash_flow = get_val(q_cf, "Free Cash Flow")
            total_debt = get_val(q_bs, "Total Debt") or get_val(q_bs, "Long Term Debt")
            cash_equivalents = get_val(q_bs, "Cash And Cash Equivalents")

            summary_string = (
                f"Rev: {revenue} | NetInc: {net_income} | OCF: {operating_cash_flow} | "
                f"FCF: {free_cash_flow} | Debt: {total_debt} | Cash: {cash_equivalents}"
            )

            # 3. Structure Dossier
            dossier = {
                "symbol": symbol,
                "clean_symbol": clean_sym,
                "market": "US" if ".NS" not in symbol and ".BO" not in symbol else "INDIA",
                "period_ending": date_str,
                "harvested_at": datetime.datetime.now().isoformat(),
                "upcoming_earnings_date": self.get_upcoming_earnings_date(symbol),
                "key_metrics_summary": summary_string,
                "income_statement_highlights": {
                    row: get_val(q_fin, row)
                    for row in q_fin.index[:8]
                },
                "balance_sheet_highlights": {
                    row: get_val(q_bs, row)
                    for row in q_bs.index[:8]
                } if q_bs is not None and not q_bs.empty else {},
                "cash_flow_highlights": {
                    row: get_val(q_cf, row)
                    for row in q_cf.index[:8]
                } if q_cf is not None and not q_cf.empty else {},
            }

            # 4. Save to Disk
            file_name = f"{date_str}_financial_dossier.json"
            target_path = sym_dir / file_name
            with open(target_path, "w", encoding="utf-8") as f:
                json.dump(dossier, f, indent=2)

            relative_path = str(target_path.relative_to(PROJECT_ROOT)).replace("\\", "/")

            return {
                "symbol": symbol,
                "status": "HARVESTED_SUCCESSFULLY",
                "file_path": relative_path,
                "absolute_path": str(target_path),
                "period_ending": date_str,
                "metrics_summary": summary_string,
            }

        except Exception as e:
            return {
                "symbol": symbol,
                "status": f"ERROR: {str(e)}",
                "file_path": None,
                "metrics_summary": "Error fetching statements",
            }


def main():
    parser = argparse.ArgumentParser(description="F.R.I.D.A.Y. Financial Filings Harvester")
    parser.add_argument("--symbol", type=str, default="NVDA", help="Ticker symbol (e.g. NVDA, AAPL, TATAMOTORS.NS)")
    args = parser.parse_args()

    harvester = FinancialFilingsHarvester()
    result = harvester.harvest_financial_dossier(args.symbol)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
