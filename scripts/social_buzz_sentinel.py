#!/usr/bin/env python3
"""
F.R.I.D.A.Y. Social Buzz & FinTwit Pulse Sentinel
==================================================
Monitors social mention velocity, sentiment momentum, and retail buzz spikes
for Indian and US stock cashtags (e.g. $TATAMOTORS, $NVDA, $TSLA).

Usage:
  python scripts/social_buzz_sentinel.py --symbol NVDA
  python scripts/social_buzz_sentinel.py --symbol TATAMOTORS.NS
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


class SocialBuzzSentinel:
    """Estimates social velocity and retail sentiment buzz."""

    def evaluate_social_buzz(self, symbol: str) -> Dict[str, Any]:
        """
        Calculates social sentiment score, buzz velocity, and retail FOMO risk.
        Uses DuckDuckGo news/discussion velocity queries.
        """
        clean_sym = symbol.replace(".NS", "").replace(".BO", "").upper()
        cashtag = f"${clean_sym}"

        try:
            # Query recent mentions
            from friday_engine.aci.omniscient import OmniscientSearch
            omniscient = OmniscientSearch()
            query = f'"{cashtag}" OR "{clean_sym} stock" news discussion'
            results = omniscient.search_surface_web(query, max_results=8)

            mention_count = len(results)
            headlines = [r.get("title", "") for r in results]

            # Assess sentiment polarity in recent discussion
            bullish_keywords = ["moon", "breakout", "buy", "call", "all time high", "target", "undervalued", "gem"]
            bearish_keywords = ["dump", "crash", "sell", "put", "overvalued", "drop", "scam", "bubble"]

            bull_score = 0
            bear_score = 0
            for h in headlines:
                hl = h.lower()
                for b in bullish_keywords:
                    if b in hl: bull_score += 1
                for b in bearish_keywords:
                    if b in hl: bear_score += 1

            total_hits = bull_score + bear_score
            sentiment_index = round((bull_score - bear_score) / (total_hits + 1e-9), 2)

            buzz_level = "VERY_HIGH" if mention_count >= 7 else ("MODERATE" if mention_count >= 4 else "LOW")
            fomo_risk = "HIGH_FOMO_RISK" if bull_score >= 4 and bear_score == 0 else "NORMAL"

            return {
                "symbol": symbol,
                "cashtag": cashtag,
                "buzz_level": buzz_level,
                "sentiment_index": max(-1.0, min(1.0, sentiment_index)),
                "retail_fomo_warning": fomo_risk,
                "recent_social_headlines": headlines[:4],
                "evaluated_at": datetime.datetime.now().isoformat(),
            }

        except Exception as e:
            return {"status": "ERROR", "symbol": symbol, "message": str(e)}


def main():
    parser = argparse.ArgumentParser(description="F.R.I.D.A.Y. Social Buzz Sentinel")
    parser.add_argument("--symbol", type=str, default="NVDA", help="Ticker symbol")
    args = parser.parse_args()

    sentinel = SocialBuzzSentinel()
    res = sentinel.evaluate_social_buzz(args.symbol)
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
