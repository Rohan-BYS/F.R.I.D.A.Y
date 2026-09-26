#!/usr/bin/env python3
"""
F.R.I.D.A.Y. Competitor & Tech Stack Reverse-Engineer
=====================================================
Analyzes target websites and competitors to reverse-engineer their tech stack:
CMS, frontend frameworks, analytics providers, CDNs, and server headers.

Usage:
  python scripts/competitor_tech_scout.py --domain example.com
  python scripts/competitor_tech_scout.py --domain stripe.com
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

SCOUT_DIR = PROJECT_ROOT / "data" / "tech_scout"
SCOUT_DIR.mkdir(parents=True, exist_ok=True)


class CompetitorTechScout:
    """Reverse-engineers website infrastructure and third-party scripts."""

    def __init__(self, storage_dir: Optional[Path] = None):
        self.storage_dir = storage_dir or SCOUT_DIR

    def inspect_domain(self, domain: str) -> Dict[str, Any]:
        """Fetches headers and HTML signatures to identify technologies."""
        import urllib.request
        clean_domain = domain.replace("http://", "").replace("https://", "").strip("/")
        url = f"https://{clean_domain}"

        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 🕵️ Inspecting tech stack for: {url}...")

        detected = {
            "domain": clean_domain,
            "url": url,
            "inspected_at": datetime.datetime.now().isoformat(),
            "server": "Unknown",
            "cdn": "Direct / Unknown",
            "frontend_frameworks": [],
            "analytics_and_trackers": [],
            "cms": "Custom / Unknown",
        }

        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
            with urllib.request.urlopen(req, timeout=10) as response:
                headers = dict(response.info())
                html = response.read().decode("utf-8", errors="ignore")

                # 1. Server & CDN Headers
                server = headers.get("Server", headers.get("server", "Unknown"))
                detected["server"] = server

                cf_ray = headers.get("cf-ray") or headers.get("CF-RAY")
                if cf_ray: detected["cdn"] = "Cloudflare"
                elif "Fastly" in str(headers): detected["cdn"] = "Fastly"
                elif "Amazon" in str(headers) or "cloudfront" in str(headers).lower(): detected["cdn"] = "AWS CloudFront"

                # 2. Frontend / CMS Signatures in HTML
                html_lower = html.lower()
                if "wp-content" in html_lower or "wp-includes" in html_lower:
                    detected["cms"] = "WordPress"
                elif "shopify" in html_lower:
                    detected["cms"] = "Shopify"
                elif "webflow" in html_lower:
                    detected["cms"] = "Webflow"
                elif "framer" in html_lower:
                    detected["cms"] = "Framer"
                elif "ghost.org" in html_lower:
                    detected["cms"] = "Ghost"

                if "react" in html_lower or "_next" in html_lower:
                    detected["frontend_frameworks"].append("React / Next.js")
                if "vue" in html_lower or "_nuxt" in html_lower:
                    detected["frontend_frameworks"].append("Vue / Nuxt.js")
                if "tailwind" in html_lower:
                    detected["frontend_frameworks"].append("Tailwind CSS")

                # 3. Analytics
                if "google-analytics.com" in html_lower or "gtag" in html_lower:
                    detected["analytics_and_trackers"].append("Google Analytics (GA4)")
                if "hotjar" in html_lower:
                    detected["analytics_and_trackers"].append("Hotjar Heatmaps")
                if "mixpanel" in html_lower:
                    detected["analytics_and_trackers"].append("Mixpanel")
                if "segment.com" in html_lower:
                    detected["analytics_and_trackers"].append("Segment CDP")

            # Save report
            out_file = self.storage_dir / f"{clean_domain.replace('.', '_')}_stack.json"
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(detected, f, indent=2)

            detected["report_path"] = str(out_file.relative_to(PROJECT_ROOT)).replace("\\", "/")
            return detected

        except Exception as e:
            return {"domain": clean_domain, "status": "ERROR", "message": str(e)}


def main():
    parser = argparse.ArgumentParser(description="F.R.I.D.A.Y. Competitor Tech Scout")
    parser.add_argument("--domain", type=str, default="github.com", help="Target domain (e.g. stripe.com)")
    args = parser.parse_args()

    scout = CompetitorTechScout()
    res = scout.inspect_domain(args.domain)
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
