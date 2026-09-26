#!/usr/bin/env python3
"""
F.R.I.D.A.Y. GitHub Trending & Open-Source Radar
================================================
Surveils trending GitHub repositories, open-source AI frameworks,
and developer breakthroughs. Identifies potential tools for Tool Forge integration.

Usage:
  python scripts/github_trending_radar.py --language python
  python scripts/github_trending_radar.py --trending
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

RADAR_DIR = PROJECT_ROOT / "data" / "github_radar"
RADAR_DIR.mkdir(parents=True, exist_ok=True)


class GitHubTrendingRadar:
    """Monitors open-source trends and evaluates architectural breakthroughs."""

    def __init__(self, storage_dir: Optional[Path] = None):
        self.storage_dir = storage_dir or RADAR_DIR

    def fetch_trending(self, language: str = "python") -> List[Dict[str, Any]]:
        """Scrapes trending repositories via web query or GitHub search API."""
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 🔍 Scanning trending {language} repositories on GitHub...")

        try:
            import asyncio
            from friday_engine.aci.omniscient import OmniscientSearch
            omniscient = OmniscientSearch()
            query = f"site:github.com trending {language} AI agent LLM framework tools 2026"
            try:
                results = asyncio.run(omniscient.search_surface_web(query, max_results=8))
            except Exception:
                try:
                    from duckduckgo_search import DDGS
                    results = DDGS().text(query, max_results=8) or []
                except Exception:
                    results = []

            repos = []
            for r in results:
                url = r.get("url", "")
                if "github.com/" in url and len(url.split("/")) >= 5:
                    parts = url.split("github.com/")[1].split("/")
                    repo_id = f"{parts[0]}/{parts[1]}"
                    repos.append({
                        "repo": repo_id,
                        "url": f"https://github.com/{repo_id}",
                        "headline": r.get("title", ""),
                        "snippet": r.get("snippet", ""),
                        "category": language.upper(),
                    })

            # Save report
            now_str = datetime.datetime.now().strftime("%Y%m%d")
            out_file = self.storage_dir / f"trending_{language}_{now_str}.json"
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(repos, f, indent=2)

            return repos

        except Exception as e:
            return [{"status": "ERROR", "message": str(e)}]


def main():
    parser = argparse.ArgumentParser(description="F.R.I.D.A.Y. GitHub Trending Radar")
    parser.add_argument("--language", type=str, default="python", help="Language filter (python, typescript, rust)")
    parser.add_argument("--trending", action="store_true", help="Fetch trending AI repositories")
    args = parser.parse_args()

    radar = GitHubTrendingRadar()
    repos = radar.fetch_trending(language=args.language)
    print(json.dumps(repos, indent=2))


if __name__ == "__main__":
    main()
