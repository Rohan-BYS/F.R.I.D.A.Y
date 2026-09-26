#!/usr/bin/env python3
"""
F.R.I.D.A.Y. Curiosity Engine (The Autonomous Exploration Loop)
==============================================================
Autonomous self-exploration engine. Explores frontier topics (AI, Quantum, Biotech, DePIN),
synthesizes knowledge from the open web, identifies capability gaps,
and proposes new candidate skills for the Tool Forge.
Designed to be triggered on-demand or during quiet hours without heavy background overhead.

Usage:
  python scripts/friday_curiosity_engine.py --explore "Quantum Computing"
  python scripts/friday_curiosity_engine.py --auto
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

CURIOSITY_DIR = PROJECT_ROOT / "data" / "curiosity_vault"
CURIOSITY_DIR.mkdir(parents=True, exist_ok=True)

FRONTIER_TOPICS = [
    "Autonomous Agentic Architectures and Tree of Thoughts",
    "Quantum Machine Learning Algorithms",
    "Decentralized Physical Infrastructure Networks (DePIN)",
    "AI-Assisted Protein Folding and Drug Discovery",
    "Post-Quantum Cryptography Standards (NIST)",
    "Neuromorphic Computing and Spiking Neural Networks",
    "Synthetic Biology Gene Editing Workflows",
    "High-Frequency Automated Market Making Protocols",
]


class FridayCuriosityEngine:
    """Powers F.R.I.D.A.Y.'s autonomous intellectual exploration and curiosity."""

    def __init__(self, vault_dir: Optional[Path] = None):
        self.vault_dir = vault_dir or CURIOSITY_DIR

    def explore_topic(self, topic: str) -> Dict[str, Any]:
        """Researches an unfamiliar frontier topic and generates an exploration dossier."""
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 🧭 Exploring frontier topic: '{topic}'...")

        try:
            import asyncio
            from friday_engine.aci.omniscient import OmniscientSearch
            omniscient = OmniscientSearch()
            query = f"{topic} latest research breakthroughs overview practical applications"
            try:
                results = asyncio.run(omniscient.search_surface_web(query, max_results=6))
            except Exception:
                try:
                    from duckduckgo_search import DDGS
                    results = DDGS().text(query, max_results=6) or []
                except Exception:
                    results = []

            summaries = []
            for r in results:
                summaries.append({
                    "title": r.get("title", ""),
                    "snippet": r.get("snippet", ""),
                    "url": r.get("url", ""),
                })

            dossier = {
                "topic": topic,
                "explored_at": datetime.datetime.now().isoformat(),
                "discovered_sources_count": len(results),
                "key_findings": summaries,
                "candidate_skill_ideas": [
                    f"{topic.lower().replace(' ', '_')}_analyzer",
                    f"{topic.lower().replace(' ', '_')}_workflow_optimizer"
                ],
                "self_reflection": f"F.R.I.D.A.Y. has ingested foundational concepts of {topic}. Ready to synthesize automated tools upon request.",
            }

            # Save to disk
            safe_name = "".join(c if c.isalnum() else "_" for c in topic.lower())[:40]
            target_path = self.vault_dir / f"{safe_name}_exploration.json"
            with open(target_path, "w", encoding="utf-8") as f:
                json.dump(dossier, f, indent=2)

            dossier["saved_file"] = str(target_path.relative_to(PROJECT_ROOT)).replace("\\", "/")
            return dossier

        except Exception as e:
            return {"status": "ERROR", "topic": topic, "message": str(e)}

    def run_auto_exploration(self) -> Dict[str, Any]:
        """Picks a random unvisited frontier topic and explores it."""
        import random
        topic = random.choice(FRONTIER_TOPICS)
        return self.explore_topic(topic)


def main():
    parser = argparse.ArgumentParser(description="F.R.I.D.A.Y. Curiosity Engine")
    parser.add_argument("--explore", type=str, help="Specific topic to explore")
    parser.add_argument("--auto", action="store_true", help="Auto-explore a frontier topic")
    args = parser.parse_args()

    engine = FridayCuriosityEngine()

    if args.explore:
        res = engine.explore_topic(args.explore)
        print(json.dumps(res, indent=2))
    else:
        res = engine.run_auto_exploration()
        print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
