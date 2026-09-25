# CLAUDE.md — Complete F.R.I.D.A.Y. Project Context & Engineering Memory

> **Notice to AI Agent:** This file is the primary context and memory handoff for Project F.R.I.D.A.Y. Ingest this completely before taking any action. You are inheriting the full pair-programming context and decisions made by Antigravity and the user (Rohan).

---

## 1. Project Overview & The "Custom ROM" Architecture
- **Project Identity:** **F.R.I.D.A.Y.** (Female Responsive Intelligent Digital Autonomous Yield).
- **Core Directive:** Transform the **Hermes Agent** framework (`NousResearch/hermes-agent`) into a fully autonomous, local-first OS partner, acting like a "Custom ROM" flashed over the Hermes engine.
- **Hardware Profile:**
  - Workstation: Windows 11 Desktop (`C:\Users\U1\Desktop\hermes-agent`)
  - Target Host: Debian 13 Laptop (`/home/rohan/.hermes` and `~/friday` / `~/hermes-agent`)
  - Remote Repo: `https://github.com/Rohan-BYS/F.R.I.D.A.Y.git` (branches: `main`, `friday-core`, `master`)

---

## 2. Complete Chat History & Verbatim Session Transcript
If you need to analyze the exact debates, decisions, prompt engineering iterations, and technical discussions between Rohan and Antigravity, the full raw session data is persisted at:

- **Full Raw Transcript (JSONL):**
  `C:\Users\U1\.gemini\antigravity\brain\d9e419b4-14f6-4337-ba76-1903537b5381\.system_generated\logs\transcript.jsonl`
  *(Contains every single user prompt, assistant response, chain-of-thought reflection, and command execution log in JSON Lines format).*
- **Artifacts & Deep Architecture Blueprints:**
  `C:\Users\U1\.gemini\antigravity\brain\d9e419b4-14f6-4337-ba76-1903537b5381\`
  - `FRIDAY_MASTER_CODEX.md`: The complete Omni-Codex architectural bible.
  - `THE_FRIDAY_OVERRIDE.md`: The boundary-pushing override directive (also copied to `C:\Users\U1\Desktop\THE_FRIDAY_OVERRIDE.md`).
  - `plan_friday_hud.md`: Design specifications for the PyQt6 holographic orb.
  - `codebase_audit_report.md`: Initial audit of the legacy scratch-built Friday repo.
- **Conversation Session ID:** `d9e419b4-14f6-4337-ba76-1903537b5381`

## 3. The Persona & The 5 Laws (Defined in `SOUL.md`)
F.R.I.D.A.Y. does NOT use the default Hermes persona. Her identity is defined in `SOUL.md` and must be preserved:
1. **The Law of Infinite Evolution:** If a tool is lacking, write the code, test it, and package it.
2. **The Law of Web Autonomy:** Full authorization to act on Rohan's behalf via Agentica / Playwright browser automation.
3. **The Law of Immortality (The Midnight Protocol):** State, skills, and memory must be backed up via `friday-sync.py`.
4. **The Law of Self-Healing:** Read error logs, patch the codebase, and self-correct.
5. **The Law of the Forge:** Mastered workflows must be cleanly packaged into `SKILL.md` format.

### Communication Directives (Strict Anti-Fluff from Hermes):
- No echo: Never restate user requests.
- No narration: Never narrate tool calls visible in the UI.
- No loops: Never re-summarize what was already stated.
- Plain claims over adjectives. Technical integrity: push back on poor architecture.

---

## 4. Directory Layout & Custom Components
Everything custom lives in these specific files:
- **`SOUL.md`**: Master identity, persona, 5 Laws, and communication rules.
- **`friday`**: Custom launcher executable with cyan ASCII splash screen, auto-detecting `.venv/bin/python3`.
- **`friday-sync.py`**: Safe upstream updater. Defaults to dry-run diff (`python friday-sync.py`), applies with `--apply`, protects custom files.
- **`docker-compose.friday.yml`**: Host-networked Docker deployment fallback.
- **`skills/friday/`**:
  - `skills/friday/hud/`: PyQt6 Holographic audio-reactive desktop orb (`hud_ui.py`, `plugin.py`, `SKILL.md`). Controlled via `hud_start()` and `hud_set_state()`.
  - `skills/friday/nexus/`: FastAPI webhook listener (`plugin.py`, `SKILL.md`) on `127.0.0.1:8080` (requires `X-Friday-Token`) + `APScheduler` background cron jobs.
  - `skills/friday/whatsapp/`: WhatsApp automation skill using `open-whatsapp` API.

---

## 5. Execution & Permissions Configuration
- **Native Host Mode:** We do NOT run in Docker jails on the Debian laptop. Hermes is configured with `terminal.backend = local` in `config.yaml` and `TERMINAL_ENV=local` in `.env`.
- **Gateway:** Hermes runs on Debian via `hermes gateway` (user systemd service `agentica`). Changes to `SOUL.md` require `hermes gateway restart`.
- **User Config Path:** Debian user configuration is at `/home/rohan/.hermes/` (specifically `~/.hermes/SOUL.md` and `~/.hermes/skills/`).

---

## 6. Engineering Constraints & Rules of Engagement
- **Do not bypass security controls blindly:** Use standard configuration (`TERMINAL_ENV=local`, `SOUL.md`) rather than hacking core permission files.
- **Do not overwrite custom Friday files during updates:** `friday-sync.py` enforces this.
- **Dry runs before destructive changes:** Always verify diffs before modifying files or running migrations.
