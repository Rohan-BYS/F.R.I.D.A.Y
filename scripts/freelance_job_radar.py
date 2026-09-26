#!/usr/bin/env python3
"""
F.R.I.D.A.Y. Freelance Job & Remote Task Arbitrage Radar
=========================================================
Surveils remote freelance job boards (Upwork, RemoteOK, GitHub Jobs feeds)
for high-value automation, web scraping, and AI development tasks.
Synthesizes winning technical proposals tailored to client requirements.

Usage:
  python scripts/freelance_job_radar.py --query "Python web scraping"
  python scripts/freelance_job_radar.py --query "AI agent automation"
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

if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

JOBS_DIR = PROJECT_ROOT / "data" / "freelance_leads"
JOBS_DIR.mkdir(parents=True, exist_ok=True)


class FreelanceJobRadar:
    """Surveils freelance tasks and formulates competitive technical bids."""

    def __init__(self, storage_dir: Optional[Path] = None):
        self.storage_dir = storage_dir or JOBS_DIR

    def search_tasks(self, query: str) -> List[Dict[str, Any]]:
        """Searches live freelance opportunities and structures actionable proposals."""
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 💼 Searching remote opportunities for: '{query}'...")

        try:
            import asyncio
            from friday_engine.aci.omniscient import OmniscientSearch
            omniscient = OmniscientSearch()
            search_q = f"site:upwork.com/freelance-jobs OR site:remoteok.com '{query}' hiring 2026"
            try:
                results = asyncio.run(omniscient.search_surface_web(search_q, max_results=5))
            except Exception:
                try:
                    from duckduckgo_search import DDGS
                    results = DDGS().text(search_q, max_results=5) or []
                except Exception:
                    results = []

            leads = []
            for r in results:
                title = r.get("title", "")
                snippet = r.get("snippet", "")
                url = r.get("url", "")

                proposal_template = (
                    f"Hi there,\n\n"
                    f"I reviewed your requirement regarding '{title}'. "
                    f"Our autonomous development framework can deliver an end-to-end solution with:\n"
                    f"- High-concurrency async Python pipeline (zero rate-limiting)\n"
                    f"- Automated error-handling and SQLite/Parquet local persistence\n"
                    f"- Clean, modular documentation and easy deployment\n\n"
                    f"Ready to deliver a functioning prototype within 24 hours."
                )

                leads.append({
                    "title": title,
                    "url": url,
                    "summary": snippet,
                    "suggested_proposal": proposal_template,
                })

            # Save leads
            safe_q = "".join(c if c.isalnum() else "_" for c in query.lower())[:30]
            out_file = self.storage_dir / f"{safe_q}_leads.json"
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(leads, f, indent=2)

            return leads

        except Exception as e:
            return [{"status": "ERROR", "message": str(e)}]


def main():
    parser = argparse.ArgumentParser(description="F.R.I.D.A.Y. Freelance Job Radar")
    parser.add_argument("--query", type=str, default="Python Playwright automation", help="Target skill query")
    args = parser.parse_args()

    radar = FreelanceJobRadar()
    leads = radar.search_tasks(args.query)
    print(json.dumps(leads, indent=2))


if __name__ == "__main__":
    main()
