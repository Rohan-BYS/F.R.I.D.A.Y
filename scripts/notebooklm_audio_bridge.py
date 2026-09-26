#!/usr/bin/env python3
"""
F.R.I.D.A.Y. Google NotebookLM & Audio Deep-Dive Bridge
======================================================
Prepares and formats complex research dossiers (financial filings, curiosity reports)
into structured source documents optimized for Google NotebookLM ingestion,
enabling one-click generation of viral multi-speaker Audio Overviews (Podcasts).

Usage:
  python scripts/notebooklm_audio_bridge.py --source-file "data/curiosity_vault/quantum_machine_learning_exploration.json"
  python scripts/notebooklm_audio_bridge.py --topic "Nvidia Blackwell Architecture"
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

NOTEBOOK_DIR = PROJECT_ROOT / "data" / "notebooklm_exports"
NOTEBOOK_DIR.mkdir(parents=True, exist_ok=True)


class NotebookLMBridge:
    """Prepares structured knowledge sources for Google NotebookLM."""

    def __init__(self, export_dir: Optional[Path] = None):
        self.export_dir = export_dir or NOTEBOOK_DIR

    def prepare_source_document(self, topic: str, content: str) -> Dict[str, Any]:
        """Formats unstructured content into a high-density, citation-rich NotebookLM source markdown."""
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 🎙️ Preparing NotebookLM Deep-Dive document for: '{topic}'...")

        timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        slug = "".join(c if c.isalnum() else "_" for c in topic.lower())[:30]
        out_file = self.export_dir / f"{slug}_notebooklm_source.md"

        formatted_doc = f"""# Comprehensive Briefing: {topic}
*Curated by F.R.I.D.A.Y. Autonomous Intelligence Engine*
*Date:* {datetime.datetime.now().strftime('%B %d, %Y')}

---

## 📌 Executive Abstract
This briefing compiles essential structural, economic, and technical dimensions regarding **{topic}**. Designed specifically for Google NotebookLM ingestion to produce comprehensive multi-speaker Audio Overviews.

## 🔍 Core Thematic Pillars
{content}

## 📊 Strategic Implications & Future Trajectory
1. **Immediate Disruption:** Near-term operational leverage and competitive shifts.
2. **Second-Order Effects:** Systemic ripple effects across related industries and supply chains.
3. **Core Conclusion:** The asymmetric upside belongs to architectures capable of continuous, autonomous self-adaptation.

---
*Optimized for NotebookLM 'Generate Audio Overview'. Copy or upload this source file directly.*
"""

        with open(out_file, "w", encoding="utf-8") as f:
            f.write(formatted_doc)

        return {
            "status": "NOTEBOOKLM_SOURCE_READY",
            "topic": topic,
            "source_markdown_file": str(out_file.relative_to(PROJECT_ROOT)).replace("\\", "/"),
            "instructions": (
                "Upload this .md file to notebooklm.google.com as a source, "
                "then click 'Generate Audio Overview' for a viral, two-host Deep Dive conversation!"
            ),
        }


def main():
    parser = argparse.ArgumentParser(description="F.R.I.D.A.Y. NotebookLM Audio Bridge")
    parser.add_argument("--topic", type=str, default="The Rise of Autonomous AI Agents in 2026", help="Briefing topic")
    parser.add_argument("--content", type=str, default="AI agents have evolved from passive query-response LLMs into fully recursive entities equipped with verified terminals, persistent knowledge graphs, and dynamic tool synthesis.", help="Briefing body")
    args = parser.parse_args()

    bridge = NotebookLMBridge()
    res = bridge.prepare_source_document(args.topic, args.content)
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
