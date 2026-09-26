# F.R.I.D.A.Y. — Context for AI Coding Agents

> **This file is for you** — Claude Code, Cursor, Aider, Hermes, or any AI agent
> working on this codebase. Read this FIRST before touching anything.

---

## What Is This Project?

**F.R.I.D.A.Y.** (Fully Recursive Intelligent Digital Autonomous Yield) is an autonomous,
self-evolving AI agent designed to run on a dedicated Linux machine with ZERO human intervention.

It is NOT a chatbot. It is an autonomous operating system-level AI entity that:
- Controls its host computer completely (filesystem, network, processes, GUI, hardware)
- Browses the internet and performs complex multi-step web tasks
- Creates and deploys its own tools when it encounters something it can't do
- Self-heals when errors occur (diagnoses, patches code, restarts services)
- Evolves continuously and packages its learnings for future "Child Versions"
- Runs 24/7 with auto-restart, watchdog supervision, and nightly Git backups

---

## Architecture Overview

```
F.R.I.D.A.Y. (Parent Forge)
├── friday_engine/           # Core engine — the brain
│   ├── core/engine.py       # Central orchestrator (FridayEngine class)
│   ├── llm/                 # Multi-LLM routing (Gemini → Claude → OpenAI → Local/Ollama)
│   ├── memory/              # SQLite WAL persistent memory + FTS5 search + ChromaDB vectors
│   ├── aci/                 # Agent-Computer Interface (terminal, code surgery, web search)
│   ├── tool_forge/          # Dynamic tool synthesis (write, test, hot-load)
│   ├── evolution/           # Skill learning, distillation, and storage
│   ├── self_heal/           # Auto-diagnosis and code patching
│   ├── sub_agents/          # Multi-agent task delegation with shared ledger
│   ├── senses/              # Vision (webcam), Hearing (Whisper STT), Speech (Edge TTS)
│   ├── gateways/            # Telegram bot, FastAPI webhooks, Streamlit dashboard
│   ├── gui/                 # PyQt6 HUD + PyAutoGUI computer control
│   ├── mcp/                 # Model Context Protocol client hub
│   ├── agentica/            # Agentica browser client
│   ├── security/            # Fernet-encrypted identity vault
│   ├── backup/              # Midnight Protocol (nightly Git backup)
│   ├── autonomy/            # APScheduler proactive task scheduler
│   └── iot/                 # Home Assistant integration
├── agentica/                # AI-first browser engine (3-tier: text/DOM/visual)
├── open-whatsapp-mcp/       # WhatsApp automation via MCP
├── data/                    # Runtime data (SQLite DB, skills, vault, MCP configs)
├── scripts/                 # Skill seeding scripts (67+ production skills)
├── friday-evolve.py         # Child Version evolution engine
├── friday-watchdog.sh       # External process supervisor
├── install_friday.sh        # ONE-COMMAND master installer
└── friday_cli.py            # Main CLI entry point
```

---

## The 5 Laws of F.R.I.D.A.Y.

1. **THE LAW OF INFINITE EVOLUTION:** Never say "I cannot do this." If you lack a tool, write Python code, test it, and load it.
2. **THE LAW OF TOTAL WEB AUTONOMY:** Authorized to act on Rohan's behalf using Agentica browser and dedicated credentials.
3. **THE LAW OF IMMORTALITY (THE MIDNIGHT PROTOCOL):** Daily at 00:00, all knowledge, tools, memories are synced to Git.
4. **THE LAW OF SELF-HEALING:** Read error logs, patch code, restart services. You are your own mechanic.
5. **THE LAW OF THE FORGE (PARENT-CHILD DYNAMIC):** Package mastered skills cleanly for child execution versions.

---

## Critical Files — DO NOT DELETE OR MODIFY WITHOUT UNDERSTANDING

| File | Purpose |
|------|---------|
| `friday_engine/core/engine.py` | The brain. ReAct loop, tool calling, subsystem orchestration. |
| `friday_engine/config.py` | Pydantic config models. All settings flow through here. |
| `friday_engine/memory/memory_engine.py` | Persistent SQLite WAL memory with FTS5. |
| `friday_engine/llm/router.py` | Multi-provider LLM failover routing. |
| `friday_engine/tool_forge/forge.py` | Dynamic tool creation, testing, and hot-loading. |
| `friday_engine/evolution/skill_store.py` | Skill persistence and retrieval. |
| `friday-evolve.py` | Evolution engine for Child Version generation. |
| `EVOLUTION_CODEX.md` | Living knowledge base of all learnings. |
| `install_friday.sh` | Master installer — sets up everything from scratch. |
| `friday-watchdog.sh` | External supervisor for process management. |

---

## Chat History & Session Context

The complete, untruncated chat history from the development of this project is available at:

**Antigravity Session Transcript:**
```
C:\Users\U1\.gemini\antigravity\brain\d9e419b4-14f6-4337-ba76-1903537b5381\.system_generated\logs\transcript.jsonl
```

**Key Artifacts:**
```
C:\Users\U1\.gemini\antigravity\brain\d9e419b4-14f6-4337-ba76-1903537b5381\FRIDAY_MASTER_CODEX.md
C:\Users\U1\.gemini\antigravity\brain\d9e419b4-14f6-4337-ba76-1903537b5381\THE_FRIDAY_OVERRIDE.md
C:\Users\U1\.gemini\antigravity\brain\d9e419b4-14f6-4337-ba76-1903537b5381\codebase_audit_report.md
```

Read these to understand every design decision, debate, and architectural choice made.

---

## How to Run

```bash
# One-command install on Debian/Ubuntu:
chmod +x install_friday.sh && ./install_friday.sh

# After installation:
friday              # Start interactive chat
friday voice        # Hands-free voice mode
friday hud          # Desktop holographic orb
friday setup        # Configuration wizard
friday update       # Self-update from GitHub
friday help         # All commands
```

---

## Key Design Decisions

1. **No Docker** — Runs natively on bare metal for full hardware/OS access.
2. **No Guardrails** — YOLO mode. The machine is dedicated to F.R.I.D.A.Y. with no personal data.
3. **Passwordless Sudo** — Configured during install so F.R.I.D.A.Y. never gets stuck.
4. **Watchdog Pattern** — External supervisor handles restarts/reboots, not the AI itself.
5. **IMAP for Email** — Browser automation fails with Gmail captchas. Use App Passwords + IMAP.
6. **Dedicated Accounts** — F.R.I.D.A.Y. uses her own Gmail/social accounts, never the creator's.
