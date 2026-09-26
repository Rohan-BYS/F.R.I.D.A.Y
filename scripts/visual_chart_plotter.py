#!/usr/bin/env python3
"""
F.R.I.D.A.Y. Visual Candlestick & Indicator Chart Plotter
=========================================================
Generates high-resolution candlestick chart images (PNG) with 9/21 EMA overlays,
volume bars, and RSI momentum sub-panels. Ready for sending to Telegram or Desktop HUD.

Usage:
  python scripts/visual_chart_plotter.py --symbol NVDA --period 5d --interval 15m
  python scripts/visual_chart_plotter.py --symbol TATAMOTORS.NS --period 1mo --interval 1d
"""

import os
import sys
import argparse
import datetime
from pathlib import Path
from typing import Dict, Optional, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

CHARTS_DIR = PROJECT_ROOT / "data" / "charts"
CHARTS_DIR.mkdir(parents=True, exist_ok=True)


class VisualChartPlotter:
    """Renders visual market charts to local PNG images."""

    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or CHARTS_DIR

    def plot_candlestick_chart(
        self,
        symbol: str,
        period: str = "5d",
        interval: str = "15m",
        title: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Fetches price history and renders a candlestick PNG chart with EMAs and RSI.
        Uses matplotlib/mplfinance or pandas/pillow.
        """
        try:
            import yfinance as yf
            import pandas as pd
            import numpy as np

            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period, interval=interval)

            if df.empty:
                return {"status": "ERROR", "message": f"No price history for {symbol}."}

            # Calculate indicators
            df["EMA_9"] = df["Close"].ewm(span=9, adjust=False).mean()
            df["EMA_21"] = df["Close"].ewm(span=21, adjust=False).mean()

            # RSI
            delta = df["Close"].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / (loss + 1e-9)
            df["RSI"] = 100 - (100 / (1 + rs))

            # Matplotlib plotting
            import matplotlib
            matplotlib.use("Agg")  # Headless backend
            import matplotlib.pyplot as plt
            import matplotlib.dates as mdates

            fig, (ax1, ax2) = plt.subplots(
                2, 1, figsize=(12, 7), gridspec_kw={"height_ratios": [3, 1]}, sharex=True
            )
            fig.patch.set_facecolor("#121824")
            ax1.set_facecolor("#182234")
            ax2.set_facecolor("#182234")

            # Candlesticks
            width = 0.6
            width2 = 0.1
            up = df[df.Close >= df.Open]
            down = df[df.Close < df.Open]

            x_axis = range(len(df))

            # Up candles (Green)
            ax1.vlines(up.index, up.Low, up.High, color="#00E676", linewidth=1)
            ax1.vlines(up.index, up.Open, up.Close, color="#00E676", linewidth=4)

            # Down candles (Red)
            ax1.vlines(down.index, down.Low, down.High, color="#FF1744", linewidth=1)
            ax1.vlines(down.index, down.Open, down.Close, color="#FF1744", linewidth=4)

            # EMAs
            ax1.plot(df.index, df["EMA_9"], color="#00E5FF", label="9 EMA", linewidth=1.2)
            ax1.plot(df.index, df["EMA_21"], color="#FFD600", label="21 EMA", linewidth=1.2)

            chart_title = title or f"{symbol} ({interval} Interval) — F.R.I.D.A.Y. Visual Engine"
            ax1.set_title(chart_title, color="#FFFFFF", fontsize=13, fontweight="bold", pad=12)
            ax1.grid(True, color="#25354F", linestyle="--", alpha=0.5)
            ax1.tick_params(colors="#8BA1B7")
            ax1.legend(loc="upper left", facecolor="#121824", edgecolor="#25354F", labelcolor="#FFFFFF")

            # RSI Sub-plot
            ax2.plot(df.index, df["RSI"], color="#E040FB", label="RSI(14)", linewidth=1.2)
            ax2.axhline(70, color="#FF1744", linestyle="--", alpha=0.5)
            ax2.axhline(30, color="#00E676", linestyle="--", alpha=0.5)
            ax2.set_ylabel("RSI", color="#8BA1B7")
            ax2.set_ylim(10, 90)
            ax2.grid(True, color="#25354F", linestyle="--", alpha=0.5)
            ax2.tick_params(colors="#8BA1B7")

            # Format X dates
            ax2.xaxis.set_major_formatter(mdates.DateFormatter("%d %b %H:%M"))
            fig.autofmt_xdate()

            # Save file
            now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            clean_sym = symbol.replace(".", "_")
            out_file = self.output_dir / f"{clean_sym}_{now_str}.png"
            plt.tight_layout()
            plt.savefig(out_file, dpi=120, facecolor=fig.get_facecolor(), edgecolor="none")
            plt.close(fig)

            rel_path = str(out_file.relative_to(PROJECT_ROOT)).replace("\\", "/")
            return {
                "status": "SUCCESS",
                "symbol": symbol,
                "period": period,
                "interval": interval,
                "file_path": rel_path,
                "absolute_path": str(out_file),
                "last_price": round(float(df["Close"].iloc[-1]), 2),
                "last_rsi": round(float(df["RSI"].iloc[-1]), 2),
            }

        except Exception as e:
            return {"status": "ERROR", "message": str(e)}


def main():
    parser = argparse.ArgumentParser(description="F.R.I.D.A.Y. Visual Chart Plotter")
    parser.add_argument("--symbol", type=str, default="NVDA", help="Ticker symbol")
    parser.add_argument("--period", type=str, default="5d", help="Data period (e.g. 1d, 5d, 1mo, 1y)")
    parser.add_argument("--interval", type=str, default="15m", help="Candle timeframe (e.g. 5m, 15m, 1h, 1d)")
    args = parser.parse_args()

    plotter = VisualChartPlotter()
    res = plotter.plot_candlestick_chart(args.symbol, period=args.period, interval=args.interval)
    import json
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
