#!/usr/bin/env python3
"""
F.R.I.D.A.Y. Human-Like Introspection, Backlinks & MCP Skills Seeder
===================================================================
Seeds 4 specialized skills into data/skills/:
1. human_like_nightly_introspection
2. autonomous_backlink_builder
3. notebooklm_audio_deepdive_bridge
4. dynamic_mcp_hotplug_manager
"""

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = PROJECT_ROOT / "data" / "skills"
SKILLS_DIR.mkdir(parents=True, exist_ok=True)

if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SKILLS = [
    {
        "id": "human_like_nightly_introspection",
        "name": "Human-Like Nightly Introspection & Self-Correction",
        "category": "Meta-Cognitive Autonomy",
        "description": "Reviews all daily execution traces, identifies mistakes, synthesizes root causes, and permanently patches heuristics into EVOLUTION_CODEX.md like a human learner.",
    },
    {
        "id": "autonomous_backlink_builder",
        "name": "Autonomous Backlink Prospector & Campaign Builder",
        "category": "SEO & Growth",
        "description": "Formulates 50-link contextual backlink distribution campaigns across high-DA tech portals, generating natural anchor variations to avoid spam penalties.",
    },
    {
        "id": "notebooklm_audio_deepdive_bridge",
        "name": "Google NotebookLM & Audio Deep-Dive Bridge",
        "category": "Media & Synthesis",
        "description": "Formats research dossiers into NotebookLM-ready source documents to trigger Google's multi-speaker Audio Overviews (Podcasts).",
    },
    {
        "id": "dynamic_mcp_hotplug_manager",
        "name": "Dynamic MCP Hot-Plug & Protocol Manager",
        "category": "Architecture & Protocols",
        "description": "Discovers, connects, and hot-plugs Model Context Protocol (MCP) servers (Puppeteer, SQLite, GitHub, Fetch) at runtime without restarts.",
    },
]


def seed():
    print(f"\n🌱 Seeding {len(SKILLS)} Introspection & MCP Skills...")
    for s in SKILLS:
        s_dir = SKILLS_DIR / s["id"]
        s_dir.mkdir(parents=True, exist_ok=True)
        s_file = s_dir / "SKILL.md"

        content = f"""---
name: {s["id"]}
display_name: {s["name"]}
category: {s["category"]}
version: 1.0.0
description: {s["description"]}
---

# {s["name"]}

## Category
**{s["category"]}**

## Overview
{s["description"]}

## Operational Directives
1. Continuous Evolution: Runs as a standing daily midnight routine to ensure continuous self-correction and adaptation.
2. Safe Execution: Formulates structured ledgers before making any external network requests or tool adjustments.
"""
        with open(s_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✓ [{s['category']}] {s['name']} -> {s['id']}/SKILL.md")

    print(f"\n✅ All {len(SKILLS)} skills successfully seeded into {SKILLS_DIR}!")


if __name__ == "__main__":
    seed()
