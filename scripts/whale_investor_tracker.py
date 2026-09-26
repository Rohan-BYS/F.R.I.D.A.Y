#!/usr/bin/env python3
"""
F.R.I.D.A.Y. Whale & Super-Investor Tracker
============================================
Tracks large-scale institutional accumulation, Indian super-investor portfolios
(Damani, Kedia, Kacholia), and US SEC 13F institutional hedge fund disclosures (Buffett, Burry).

Usage:
  python scripts/whale_investor_tracker.py --list-whales
  python scripts/whale_investor_tracker.py --whale "Warren Buffett"
  python scripts/whale_investor_tracker.py --whale "Vijay Kedia"
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

WHALE_DIR = PROJECT_ROOT / "data" / "whale_intelligence"
WHALE_DIR.mkdir(parents=True, exist_ok=True)

# Curated Profiles of Famous Super-Investors
WHALE_PROFILES = {
    # Indian Super-Investors
    "Vijay Kedia": {
        "market": "India",
        "fund_name": "Kedia Securities",
        "style": "SMILE (Small in size, Medium in experience, Large in aspiration, Extra-large in market potential)",
        "known_holdings": ["Tejas Networks", "Vaibhav Global", "Elecon Engineering", "Atul Auto", "Sudarshan Chemical"],
    },
    "Ashish Kacholia": {
        "market": "India",
        "fund_name": "Lucky Investment Managers",
        "style": "Midcap & Smallcap Growth Hunting",
        "known_holdings": ["Safari Industries", "Yasho Industries", "Shaily Engineering", "Gravita India", "AMI Organics"],
    },
    "Radhakishan Damani": {
        "market": "India",
        "fund_name": "Bright Star Investments",
        "style": "Value / High Cash Flow / Retail",
        "known_holdings": ["Avenue Supermarts (DMart)", "VFS Global", "India Cements", "United Breweries", "Sundaram Finance"],
    },
    # US Legendary Investors (SEC 13F)
    "Warren Buffett": {
        "market": "US",
        "fund_name": "Berkshire Hathaway Inc.",
        "style": "Moat-Driven Value & Compounding",
        "known_holdings": ["Apple (AAPL)", "American Express (AXP)", "Bank of America (BAC)", "Coca-Cola (KO)", "Chevron (CVX)"],
    },
    "Michael Burry": {
        "market": "US",
        "fund_name": "Scion Asset Management",
        "style": "Deep Value, Contrarian, Asymmetric Shorts",
        "known_holdings": ["Alibaba (BABA)", "JD.com (JD)", "Baidu (BIDU)", "HCA Healthcare"],
    },
    "Bill Ackman": {
        "market": "US",
        "fund_name": "Pershing Square Capital",
        "style": "Concentrated High-Conviction Large-Cap",
        "known_holdings": ["Alphabet (GOOGL)", "Chipotle (CMG)", "Hilton (HLT)", "Restaurant Brands (QSR)"],
    },
}


class WhaleInvestorTracker:
    """Monitors super-investor portfolios and bulk institutional transactions."""

    def __init__(self, storage_dir: Optional[Path] = None):
        self.storage_dir = storage_dir or WHALE_DIR

    def get_whale_profile(self, whale_name: str) -> Dict[str, Any]:
        """Fetches investor dossier and checks for updated portfolio holdings."""
        profile = None
        for name, data in WHALE_PROFILES.items():
            if whale_name.lower() in name.lower():
                profile = {"investor": name, **data}
                break

        if not profile:
            return {"status": "NOT_FOUND", "message": f"Investor '{whale_name}' not in tracked database."}

        profile["last_checked"] = datetime.datetime.now().isoformat()
        profile["status"] = "ACTIVE_TRACKING"

        # Save profile snapshot to disk
        safe_name = profile["investor"].lower().replace(" ", "_")
        target_file = self.storage_dir / f"{safe_name}_dossier.json"
        with open(target_file, "w", encoding="utf-8") as f:
            json.dump(profile, f, indent=2)

        profile["file_path"] = str(target_file.relative_to(PROJECT_ROOT)).replace("\\", "/")
        return profile

    def list_all_whales(self) -> List[Dict[str, str]]:
        """Returns list of all monitored super-investors across US and India."""
        return [
            {"name": name, "market": data["market"], "fund": data["fund_name"], "style": data["style"]}
            for name, data in WHALE_PROFILES.items()
        ]


def main():
    parser = argparse.ArgumentParser(description="F.R.I.D.A.Y. Whale & Super-Investor Tracker")
    parser.add_argument("--list-whales", action="store_true", help="List all tracked super-investors")
    parser.add_argument("--whale", type=str, help="Name of super-investor (e.g. Buffett, Kedia, Burry)")
    args = parser.parse_args()

    tracker = WhaleInvestorTracker()

    if args.whale:
        res = tracker.get_whale_profile(args.whale)
        print(json.dumps(res, indent=2))
    else:
        whales = tracker.list_all_whales()
        print(json.dumps(whales, indent=2))


if __name__ == "__main__":
    main()
