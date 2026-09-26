#!/usr/bin/env python3
"""
F.R.I.D.A.Y. Frontier Expansion Skills Seeder
==============================================
Seeds 14 foundational skills across Web Growth, GitHub Innovation,
Freelance Arbitrage, Media Studio, DevOps, Competitor Reverse-Engineering,
and the Curiosity Autonomous Exploration Loop.
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

FRONTIER_SKILLS = [
    {
        "id": "curiosity_autonomous_exploration_loop",
        "name": "The Curiosity Autonomous Exploration Loop",
        "category": "Meta-Cognitive Evolution",
        "description": "Explores unfamiliar frontier topics (Quantum, Biotech, DePIN), synthesizes research from the web, and plans candidate skills for the Tool Forge.",
    },
    {
        "id": "programmatic_seo_content_factory",
        "name": "Programmatic SEO & Content Cluster Factory",
        "category": "Digital Real Estate",
        "description": "Generates keyword-targeted long-tail article clusters, optimized metadata, and Schema.org JSON-LD markup ready for web publishing.",
    },
    {
        "id": "micro_saas_rapid_prototyper",
        "name": "Micro-SaaS & Utility Tool Rapid Prototyper",
        "category": "Revenue & Software",
        "description": "Scouts high-demand micro-utilities (PDF converters, calculators, formatters) and scaffolds production FastAPI/Tailwind web apps.",
    },
    {
        "id": "automated_lead_enrichment_outreach",
        "name": "Automated Lead Enrichment & Cold Outreach",
        "category": "Agency & Sales",
        "description": "Discovers corporate executive contacts, verifies email patterns, and crafts tailored cold outreach proposals.",
    },
    {
        "id": "github_trending_innovation_radar",
        "name": "GitHub Trending & Architecture Innovation Radar",
        "category": "Open-Source Intelligence",
        "description": "Surveils trending GitHub repositories across Python/Rust/TypeScript to discover breakthrough architectures and libraries.",
    },
    {
        "id": "arxiv_paperswithcode_breakthrough_scout",
        "name": "arXiv & Papers With Code Breakthrough Scout",
        "category": "AI Research",
        "description": "Scans daily computer science preprints, evaluating novel model weights, prompting methods, and algorithmic breakthroughs.",
    },
    {
        "id": "open_source_bug_bounty_hunter",
        "name": "Open-Source Bug Bounty & Issue Triage Hunter",
        "category": "Software Engineering",
        "description": "Analyzes GitHub issue trackers for good-first-issues and bug reports, formulating test cases and proposed pull request patches.",
    },
    {
        "id": "freelance_job_arbitrage_matcher",
        "name": "Freelance Job & Remote Task Arbitrage Matcher",
        "category": "Freelance & Consulting",
        "description": "Monitors remote freelance task boards, matches requirements against F.R.I.D.A.Y.'s capabilities, and drafts competitive proposals.",
    },
    {
        "id": "faceless_video_ffmpeg_pipeline",
        "name": "Faceless Video & FFmpeg Media Pipeline",
        "category": "Media & Creative",
        "description": "Generates 9:16 vertical video scripts, synthesizes Edge-TTS voiceovers, and generates FFmpeg composition pipelines for YouTube Shorts / Reels.",
    },
    {
        "id": "multi_speaker_podcast_synthesizer",
        "name": "Multi-Speaker Educational Podcast Synthesizer",
        "category": "Audio Production",
        "description": "Drafts multi-character conversational scripts on complex technical topics and synthesizes dual-speaker audio podcasts.",
    },
    {
        "id": "docker_self_hosting_devops_orchestrator",
        "name": "Docker Self-Hosting & DevOps Orchestrator",
        "category": "Infrastructure & DevOps",
        "description": "Generates and orchestrates local docker-compose stacks for self-hosted microservices (SearXNG, n8n, Redis, ChromaDB).",
    },
    {
        "id": "searxng_private_search_infrastructure",
        "name": "SearXNG Private Meta-Search Infrastructure",
        "category": "Private Search",
        "description": "Interfaces with local SearXNG instances for zero-tracking, multi-engine private web scraping without external rate limits.",
    },
    {
        "id": "competitor_tech_stack_reverse_engineer",
        "name": "Competitor Tech Stack & Infrastructure Reverse-Engineer",
        "category": "Competitive Intelligence",
        "description": "Inspects target websites to reveal their hosting providers, CDNs, CMS, frontend frameworks, and analytics trackers.",
    },
    {
        "id": "patent_landscape_prior_art_scout",
        "name": "Patent Landscape & Prior Art Scout",
        "category": "Legal & IP",
        "description": "Searches global patent registries (Google Patents, USPTO) to identify prior art and evaluate freedom-to-operate for new software concepts.",
    },
]


def seed():
    print(f"\n🌱 Seeding {len(FRONTIER_SKILLS)} Frontier Expansion Skills...")
    for s in FRONTIER_SKILLS:
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
1. On-Demand Execution: This skill operates dormant by default to preserve physical system resources.
2. Activate strictly upon user instruction, scheduled event, or curiosity loop trigger.
3. Output all artifacts to dedicated folders under `data/` and record high-level metadata in memory.
"""
        with open(s_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✓ [{s['category']}] {s['name']} -> {s['id']}/SKILL.md")

    print(f"\n✅ All {len(FRONTIER_SKILLS)} frontier expansion skills successfully seeded into {SKILLS_DIR}!")


if __name__ == "__main__":
    seed()
