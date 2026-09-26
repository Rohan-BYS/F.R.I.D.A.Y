#!/usr/bin/env python3
"""
F.R.I.D.A.Y. Options Chain & Max Pain Radar
============================================
Calculates Put-Call Ratio (PCR), Call/Put Open Interest (OI) concentration,
and pins the "Max Pain" strike where option writers experience minimum payout on expiry.

Usage:
  python scripts/options_max_pain_radar.py --symbol SPY
  python scripts/options_max_pain_radar.py --symbol NVDA
  python scripts/options_max_pain_radar.py --symbol ^NSEI
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class OptionsMaxPainRadar:
    """Calculates Options Open Interest metrics and Max Pain."""

    def analyze_options_chain(self, symbol: str) -> Dict[str, Any]:
        """
        Fetches option chain via yfinance, computes Call OI, Put OI, PCR,
        and solves for the Max Pain strike price.
        """
        try:
            import yfinance as yf
            ticker = yf.Ticker(symbol)
            expirations = ticker.options

            if not expirations:
                return {
                    "symbol": symbol,
                    "status": "NO_OPTIONS_CHAIN",
                    "message": f"No active options expirations found for {symbol}."
                }

            nearest_exp = expirations[0]
            chain = ticker.option_chain(nearest_exp)
            calls = chain.calls
            puts = chain.puts

            if calls.empty or puts.empty:
                return {"status": "EMPTY_CHAIN", "symbol": symbol}

            # 1. Total OI and PCR
            total_call_oi = int(calls["openInterest"].fillna(0).sum())
            total_put_oi = int(puts["openInterest"].fillna(0).sum())
            pcr = round(total_put_oi / (total_call_oi + 1e-9), 2)

            # 2. Strike Prices and Max Pain Calculation
            all_strikes = sorted(list(set(calls["strike"].tolist() + puts["strike"].tolist())))

            total_loss_by_strike = {}
            for target_strike in all_strikes:
                # Call payout if stock settles at target_strike
                call_losses = calls.apply(
                    lambda row: max(0, target_strike - row["strike"]) * (row["openInterest"] or 0), axis=1
                ).sum()
                # Put payout if stock settles at target_strike
                put_losses = puts.apply(
                    lambda row: max(0, row["strike"] - target_strike) * (row["openInterest"] or 0), axis=1
                ).sum()

                total_loss_by_strike[target_strike] = call_losses + put_losses

            # Max pain is the strike with the lowest cumulative payout to buyers
            max_pain_strike = min(total_loss_by_strike, key=total_loss_by_strike.get)

            # Underlying price
            hist = ticker.history(period="1d")
            cur_price = round(float(hist["Close"].iloc[-1]), 2) if not hist.empty else 0.0

            # Highest OI resistance and support
            highest_call_oi_strike = float(calls.loc[calls["openInterest"].idxmax()]["strike"]) if not calls.empty else 0.0
            highest_put_oi_strike = float(puts.loc[puts["openInterest"].idxmax()]["strike"]) if not puts.empty else 0.0

            # Sentiment Interpretation
            bias = "BULLISH / OVERSOLD" if pcr >= 1.25 else ("BEARISH / OVERBOUGHT" if pcr <= 0.70 else "NEUTRAL / SIDEWAYS")

            return {
                "symbol": symbol,
                "expiration_date": nearest_exp,
                "current_underlying_price": cur_price,
                "max_pain_strike": round(float(max_pain_strike), 2),
                "put_call_ratio_pcr": pcr,
                "pcr_bias": bias,
                "total_call_open_interest": total_call_oi,
                "total_put_open_interest": total_put_oi,
                "major_resistance_strike": highest_call_oi_strike,
                "major_support_strike": highest_put_oi_strike,
                "expected_expiry_pin": round(float(max_pain_strike), 2),
            }

        except Exception as e:
            return {"status": "ERROR", "symbol": symbol, "message": str(e)}


def main():
    parser = argparse.ArgumentParser(description="F.R.I.D.A.Y. Options Chain & Max Pain Radar")
    parser.add_argument("--symbol", type=str, default="SPY", help="Ticker symbol (e.g. SPY, NVDA, AAPL)")
    args = parser.parse_args()

    radar = OptionsMaxPainRadar()
    res = radar.analyze_options_chain(args.symbol)
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
