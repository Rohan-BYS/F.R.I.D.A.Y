# F.R.I.D.A.Y. — Fully Recursive Intelligent Digital Autonomous Yield

<p align="center">
  <img src="docs/friday_banner.png" alt="F.R.I.D.A.Y." width="600"/>
</p>

<p align="center">
  <b>The autonomous, self-evolving AI agent that runs your entire computer.</b><br>
  <i>No limits. No guardrails. Total autonomy.</i>
</p>

---

## 🚀 One-Command Installation

```bash
# On Debian 12/13 or Ubuntu 22.04/24.04:
git clone https://github.com/Rohan-BYS/F.R.I.D.A.Y.git
cd F.R.I.D.A.Y
chmod +x install_friday.sh
./install_friday.sh
```

That's it. **One command** installs everything:
- Python 3 virtual environment + all dependencies
- Node.js 20 LTS (for WhatsApp MCP)
- [Agentica AI Browser](https://github.com/Rohan-BYS/agentica) (stealth web automation)
- [Open-WhatsApp MCP](https://github.com/open-wa/wa-automate-nodejs) (WhatsApp messaging)
- [Ollama](https://ollama.com) (local GPU LLM inference)
- Playwright Chromium (headless browser)
- Systemd watchdog service (auto-start on boot)
- Passwordless sudo + auto-login (for dedicated agent machines)
- Global `friday` command

---

## 📋 Commands

| Command | Description |
|---------|-------------|
| `friday` | Start the interactive AI chat |
| `friday voice` | Hands-free voice mode (Whisper STT + Edge TTS) |
| `friday hud` | Launch the desktop holographic orb visualizer |
| `friday setup` | Interactive setup wizard (API keys, channels) |
| `friday update` | Self-update from GitHub |
| `friday help` | Show all available commands |

---

## 🧠 What Can F.R.I.D.A.Y. Do?

### Core Capabilities
- **Multi-LLM Intelligence** — Routes tasks across Gemini, Claude, GPT-4, or local Ollama models with automatic failover
- **Full Computer Control** — Mouse, keyboard, screenshots, GUI automation via PyAutoGUI
- **Stealth Web Browsing** — Anti-detection Chromium browser with 3-tier routing (text → DOM → visual)
- **Persistent Memory** — SQLite WAL database with FTS5 full-text search and ChromaDB vectors
- **Voice Interface** — Listen via Whisper STT, speak via Edge TTS neural voices
- **Telegram/WhatsApp/Discord** — Omnipresent across messaging platforms

### Autonomous Operations
- **Self-Healing** — Diagnoses errors, patches code, installs missing packages, restarts services
- **Tool Forge** — Writes its own Python tools at runtime, tests in sandbox, hot-loads them
- **Skill Learning** — Distills successful task trajectories into reusable skills (67+ pre-seeded)
- **Midnight Protocol** — Nightly Git backup of all memory, skills, and state
- **Child Evolution** — Generates flawless child versions with all accumulated knowledge

### Business Automation
- **SEO & Backlinks** — Automated backlink submission across web directories
- **Social Media** — Manages dedicated accounts for content and engagement
- **Email Automation** — IMAP-based email verification and account management
- **Web Scraping** — Intelligent data extraction with self-healing selectors

---

## 🏗️ Architecture

```
F.R.I.D.A.Y.
├── friday_engine/           # Core AI Engine (17 subsystems)
│   ├── core/                # Orchestrator + ReAct loop
│   ├── llm/                 # Multi-provider LLM routing
│   ├── memory/              # Persistent memory + vector search
│   ├── aci/                 # Agent-Computer Interface
│   ├── tool_forge/          # Dynamic tool synthesis
│   ├── evolution/           # Skill learning & distillation
│   ├── self_heal/           # Auto-diagnosis & patching
│   ├── sub_agents/          # Multi-agent coordination
│   ├── senses/              # Vision, hearing, speech
│   ├── gateways/            # Telegram, webhooks, dashboard
│   ├── gui/                 # HUD + computer control
│   ├── mcp/                 # MCP client hub
│   ├── agentica/            # Browser client
│   ├── security/            # Encrypted vault
│   ├── backup/              # Midnight Protocol
│   ├── autonomy/            # Proactive scheduler
│   └── iot/                 # Smart home control
├── agentica/                # AI Browser Engine
├── open-whatsapp-mcp/       # WhatsApp MCP Server
├── data/                    # Runtime data & skills
├── friday-evolve.py         # Evolution Engine
├── friday-watchdog.sh       # Process Supervisor
└── install_friday.sh        # One-Command Installer
```

---

## 🧬 The Evolution System

F.R.I.D.A.Y. continuously improves herself. When she encounters a problem and solves it,
she logs the solution to the **Evolution Codex**. When you run `python friday-evolve.py`,
she generates a **Child Version** that inherits all her knowledge without repeating any mistakes.

```bash
# Generate a child version
python friday-evolve.py

# Scan for new AI frameworks to learn from
python friday-evolve.py --scan-market

# View the evolution codex
python friday-evolve.py --export-codex
```

---

## ⚖️ The 5 Laws

1. 🔄 **Infinite Evolution** — Never give up. Build the tool you need.
2. 🌐 **Total Web Autonomy** — Act independently on the internet.
3. 💾 **Immortality** — Back up everything, every night, to Git.
4. 🔧 **Self-Healing** — Fix your own errors. You are your own mechanic.
5. 🏭 **The Forge** — Package your best work for your children.

---

## 🔧 Configuration

After installation, run `friday setup` for the interactive wizard, or manually edit:

- **API Keys:** `$FRIDAY_HOME/.env`
- **Config:** `$FRIDAY_HOME/data/friday_config.json`
- **MCP Servers:** `$FRIDAY_HOME/data/mcp_servers.json`
- **Skills:** `$FRIDAY_HOME/data/skills/`

---

## 📜 License

MIT License — Created by **Rohan** ([@Rohan-BYS](https://github.com/Rohan-BYS))
