#!/usr/bin/env bash
# ============================================================================
#  F.R.I.D.A.Y. — FINAL FRIDAY — ONE-COMMAND MASTER INSTALLER
#  Fully Recursive Intelligent Digital Autonomous Yield
#  
#  Usage:  curl -fsSL <your-raw-url> | bash
#     or:  chmod +x install_friday.sh && ./install_friday.sh
#
#  This script will:
#    1. Install ALL system dependencies (Python, Node.js, Git, audio, GUI, etc.)
#    2. Set up the Python virtual environment & pip dependencies
#    3. Clone & install Agentica Browser (from Rohan-BYS/agentica)
#    4. Clone & install Open-WhatsApp MCP Server (from local/open-wa)
#    5. Install Playwright Chromium with stealth deps
#    6. Install Ollama for local LLM inference (GPU support)
#    7. Configure passwordless sudo for the current user
#    8. Configure auto-login (optional, for dedicated agent machines)
#    9. Install & enable the friday-watchdog systemd service
#   10. Register the global `friday` command
#   11. Initialize data directories & default config
#
#  Supports: Debian 12/13, Ubuntu 22.04/24.04, and derivatives
#  Hardware: x86_64 with optional NVIDIA GPU (auto-detected)
# ============================================================================
set -euo pipefail

# ── Colors ──────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; RESET='\033[0m'

log()   { echo -e "${CYAN}[F.R.I.D.A.Y.]${RESET} $1"; }
ok()    { echo -e "${GREEN}[✓]${RESET} $1"; }
warn()  { echo -e "${YELLOW}[!]${RESET} $1"; }
fail()  { echo -e "${RED}[✗]${RESET} $1"; exit 1; }

FRIDAY_BANNER='
  ███████╗ ██████╗  ██╗ ██████╗   █████╗  ██╗   ██╗
  ██╔════╝ ██╔══██╗ ██║ ██╔══██╗ ██╔══██╗ ╚██╗ ██╔╝
  █████╗   ██████╔╝ ██║ ██║  ██║ ███████║  ╚████╔╝
  ██╔══╝   ██╔══██╗ ██║ ██║  ██║ ██╔══██║   ╚██╔╝
  ██║      ██║  ██║ ██║ ██████╔╝ ██║  ██║    ██║
  ╚═╝      ╚═╝  ╚═╝ ╚═╝ ╚═════╝  ╚═╝  ╚═╝    ╚═╝
  ─────────────────────────────────────────────────
  FINAL FRIDAY — One-Command Autonomous AI Installer
  ─────────────────────────────────────────────────
'

echo -e "${CYAN}${FRIDAY_BANNER}${RESET}"

# ── Pre-flight checks ──────────────────────────────────────────────────────
[[ $EUID -eq 0 ]] && fail "Do NOT run this as root. Run as your normal user (sudo will be used internally)."
command -v apt-get &>/dev/null || fail "This installer requires apt-get (Debian/Ubuntu). Exiting."

FRIDAY_HOME="${FRIDAY_HOME:-$HOME/F.R.I.D.A.Y}"
CURRENT_USER=$(whoami)

log "Installing F.R.I.D.A.Y. to: ${BOLD}$FRIDAY_HOME${RESET}"
log "Current user: ${BOLD}$CURRENT_USER${RESET}"
echo ""

# ============================================================================
# PHASE 1: System Dependencies
# ============================================================================
log "━━━ PHASE 1/10: Installing System Dependencies ━━━"

sudo apt-get update -y
sudo apt-get install -y \
    git curl wget build-essential software-properties-common \
    python3 python3-pip python3-venv python3-dev \
    libffi-dev libssl-dev libsqlite3-dev \
    ffmpeg tesseract-ocr \
    portaudio19-dev libasound2-dev alsa-utils pulseaudio \
    libgl1 libglib2.0-0 libdbus-1-3 \
    libxcb-xinerama0 libxkbcommon-x11-0 libxcb-cursor0 \
    libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 \
    libxcb-render-util0 libxcb-shape0 \
    xvfb x11-utils xdotool wmctrl scrot \
    sqlite3 sqlitebrowser \
    python3-tk jq unzip \
    2>/dev/null

ok "System dependencies installed."

# ── Node.js 20 LTS ──
if ! command -v node &>/dev/null || [[ $(node -v | cut -d. -f1 | tr -d v) -lt 18 ]]; then
    log "Installing Node.js 20 LTS..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi
ok "Node.js $(node -v) ready."

# ── NVIDIA GPU Detection (optional) ──
if lspci 2>/dev/null | grep -iq nvidia; then
    log "NVIDIA GPU detected. Ensuring CUDA toolkit is available..."
    if ! command -v nvidia-smi &>/dev/null; then
        warn "nvidia-smi not found. Install NVIDIA drivers manually for GPU acceleration."
    else
        ok "NVIDIA GPU: $(nvidia-smi --query-gpu=name --format=csv,noheader | head -1)"
    fi
else
    log "No NVIDIA GPU detected. Running in CPU-only mode."
fi

# ============================================================================
# PHASE 2: Clone or Update F.R.I.D.A.Y. Repository
# ============================================================================
log "━━━ PHASE 2/10: Setting up F.R.I.D.A.Y. Repository ━━━"

if [ -d "$FRIDAY_HOME/.git" ]; then
    log "Existing installation found. Pulling latest..."
    cd "$FRIDAY_HOME"
    git pull --ff-only || warn "Git pull failed. Continuing with existing code."
elif [ -d "$FRIDAY_HOME/friday_engine" ]; then
    log "F.R.I.D.A.Y. code found (no git). Using existing files."
else
    log "Cloning F.R.I.D.A.Y. from GitHub..."
    git clone https://github.com/Rohan-BYS/F.R.I.D.A.Y.git "$FRIDAY_HOME"
fi

cd "$FRIDAY_HOME"
ok "F.R.I.D.A.Y. codebase ready at $FRIDAY_HOME"

# ============================================================================
# PHASE 3: Python Virtual Environment & Dependencies
# ============================================================================
log "━━━ PHASE 3/10: Python Environment Setup ━━━"

if [ ! -d "$FRIDAY_HOME/.venv" ]; then
    python3 -m venv "$FRIDAY_HOME/.venv"
fi
source "$FRIDAY_HOME/.venv/bin/activate"

pip install --upgrade pip setuptools wheel 2>/dev/null

if [ -f "$FRIDAY_HOME/requirements.txt" ]; then
    pip install -r "$FRIDAY_HOME/requirements.txt" 2>/dev/null
fi

# Install critical extras that may fail on some systems
pip install pyaudio 2>/dev/null || warn "pyaudio failed — microphone input may not work."
pip install opencv-python-headless 2>/dev/null || true
pip install pyttsx3 2>/dev/null || true

ok "Python virtual environment ready. $(python --version)"

# ============================================================================
# PHASE 4: Playwright Browser Binaries
# ============================================================================
log "━━━ PHASE 4/10: Installing Playwright Chromium ━━━"

pip install playwright 2>/dev/null
python -m playwright install --with-deps chromium 2>/dev/null || warn "Playwright install had issues. Browser automation may need manual setup."

ok "Playwright Chromium installed."

# ============================================================================
# PHASE 5: Clone & Install Agentica Browser
# ============================================================================
log "━━━ PHASE 5/10: Installing Agentica AI Browser ━━━"

AGENTICA_DIR="$FRIDAY_HOME/agentica"

if [ -d "$AGENTICA_DIR/.git" ]; then
    log "Agentica already cloned. Updating..."
    cd "$AGENTICA_DIR"
    git pull --ff-only 2>/dev/null || true
elif [ -d "$AGENTICA_DIR/src" ]; then
    log "Agentica code exists (no git). Using existing files."
else
    log "Cloning Agentica from GitHub..."
    git clone https://github.com/Rohan-BYS/agentica.git "$AGENTICA_DIR"
fi

cd "$AGENTICA_DIR"

# Install Agentica's own Python dependencies
if [ -f "requirements.txt" ]; then
    source "$FRIDAY_HOME/.venv/bin/activate"
    pip install -r requirements.txt 2>/dev/null || warn "Some Agentica dependencies failed."
fi

cd "$FRIDAY_HOME"
ok "Agentica Browser installed at $AGENTICA_DIR"

# ============================================================================
# PHASE 6: Clone & Install Open-WhatsApp MCP Server
# ============================================================================
log "━━━ PHASE 6/10: Installing Open-WhatsApp MCP Server ━━━"

OPENWA_DIR="$FRIDAY_HOME/open-whatsapp-mcp"

if [ -d "$OPENWA_DIR/node_modules" ]; then
    log "Open-WhatsApp already installed."
elif [ -d "$OPENWA_DIR" ]; then
    log "Open-WhatsApp directory exists. Installing Node dependencies..."
    cd "$OPENWA_DIR"
    npm install 2>/dev/null || warn "npm install had issues."
else
    log "Creating Open-WhatsApp MCP server scaffold..."
    mkdir -p "$OPENWA_DIR/src"

    cat > "$OPENWA_DIR/package.json" << 'PKGJSON'
{
  "name": "open-whatsapp-mcp",
  "version": "1.0.0",
  "description": "WhatsApp MCP Server for F.R.I.D.A.Y.",
  "main": "src/mcp-server.js",
  "scripts": {
    "start": "node src/mcp-server.js"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.0.0",
    "@open-wa/wa-automate": "^4.71.0",
    "csv-parse": "^5.5.0",
    "dotenv": "^16.3.0"
  }
}
PKGJSON

    cd "$OPENWA_DIR"
    npm install 2>/dev/null || warn "Open-WhatsApp npm install failed. WhatsApp features need manual setup."
fi

cd "$FRIDAY_HOME"
ok "Open-WhatsApp MCP server ready at $OPENWA_DIR"

# ============================================================================
# PHASE 7: Install Ollama (Local LLM Runtime)
# ============================================================================
log "━━━ PHASE 7/10: Installing Ollama Local LLM Runtime ━━━"

if command -v ollama &>/dev/null; then
    ok "Ollama already installed: $(ollama --version 2>/dev/null || echo 'version unknown')"
else
    log "Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh 2>/dev/null || warn "Ollama installation failed. Local models need manual setup."
    if command -v ollama &>/dev/null; then
        ok "Ollama installed successfully."
    fi
fi

# ============================================================================
# PHASE 8: Configure Passwordless Sudo & Auto-Login
# ============================================================================
log "━━━ PHASE 8/10: Configuring System Autonomy ━━━"

# Passwordless sudo
SUDOERS_FILE="/etc/sudoers.d/friday-nopasswd"
if [ ! -f "$SUDOERS_FILE" ]; then
    log "Configuring passwordless sudo for $CURRENT_USER..."
    echo "$CURRENT_USER ALL=(ALL) NOPASSWD: ALL" | sudo tee "$SUDOERS_FILE" > /dev/null
    sudo chmod 440 "$SUDOERS_FILE"
    ok "Passwordless sudo configured."
else
    ok "Passwordless sudo already configured."
fi

# Auto-login (GDM3 for GNOME-based systems)
GDM_CONF="/etc/gdm3/custom.conf"
if [ -f "$GDM_CONF" ]; then
    if ! grep -q "AutomaticLoginEnable" "$GDM_CONF"; then
        log "Configuring auto-login..."
        sudo sed -i "s/\[daemon\]/[daemon]\nAutomaticLoginEnable=true\nAutomaticLogin=$CURRENT_USER/" "$GDM_CONF"
        ok "Auto-login enabled for $CURRENT_USER."
    else
        ok "Auto-login already configured."
    fi
else
    # Try LightDM
    LIGHTDM_CONF="/etc/lightdm/lightdm.conf"
    if [ -f "$LIGHTDM_CONF" ] || command -v lightdm &>/dev/null; then
        sudo mkdir -p /etc/lightdm
        sudo tee "$LIGHTDM_CONF" > /dev/null << LIGHTDM
[Seat:*]
autologin-user=$CURRENT_USER
autologin-user-timeout=0
LIGHTDM
        ok "LightDM auto-login configured."
    else
        # Console auto-login via systemd getty
        log "Configuring console auto-login via systemd..."
        sudo mkdir -p /etc/systemd/system/getty@tty1.service.d
        sudo tee /etc/systemd/system/getty@tty1.service.d/override.conf > /dev/null << GETTY
[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin $CURRENT_USER --noclear %I \$TERM
GETTY
        sudo systemctl daemon-reload
        ok "Console auto-login configured."
    fi
fi

# ============================================================================
# PHASE 9: Watchdog Supervisor & Systemd Services
# ============================================================================
log "━━━ PHASE 9/10: Installing Watchdog Supervisor ━━━"

# Create the Watchdog script
cat > "$FRIDAY_HOME/friday-watchdog.sh" << 'WATCHDOG'
#!/usr/bin/env bash
# F.R.I.D.A.Y. Watchdog Supervisor
# Monitors for restart/reboot signals and manages the friday process lifecycle.
# Signals via touch files:
#   /tmp/friday-restart  → Restart the F.R.I.D.A.Y. process
#   /tmp/friday-reboot   → Reboot the entire machine

set -u
FRIDAY_HOME="${FRIDAY_HOME:-$HOME/F.R.I.D.A.Y}"
VENV="$FRIDAY_HOME/.venv/bin/activate"
RESTART_SIGNAL="/tmp/friday-restart"
REBOOT_SIGNAL="/tmp/friday-reboot"
FRIDAY_PID=""

start_friday() {
    echo "[Watchdog] Starting F.R.I.D.A.Y. engine..."
    source "$VENV"
    cd "$FRIDAY_HOME"
    python friday_cli.py &
    FRIDAY_PID=$!
    echo "[Watchdog] F.R.I.D.A.Y. started with PID $FRIDAY_PID"
}

stop_friday() {
    if [ -n "$FRIDAY_PID" ] && kill -0 "$FRIDAY_PID" 2>/dev/null; then
        echo "[Watchdog] Stopping F.R.I.D.A.Y. (PID $FRIDAY_PID)..."
        kill "$FRIDAY_PID" 2>/dev/null
        wait "$FRIDAY_PID" 2>/dev/null || true
    fi
    FRIDAY_PID=""
}

cleanup() {
    echo "[Watchdog] Shutting down watchdog..."
    stop_friday
    rm -f "$RESTART_SIGNAL" "$REBOOT_SIGNAL"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Clean any stale signals
rm -f "$RESTART_SIGNAL" "$REBOOT_SIGNAL"

# Initial start
start_friday

# Main supervisor loop
while true; do
    # Check for reboot signal
    if [ -f "$REBOOT_SIGNAL" ]; then
        echo "[Watchdog] REBOOT signal detected!"
        rm -f "$REBOOT_SIGNAL" "$RESTART_SIGNAL"
        stop_friday
        sleep 2
        sudo reboot
        exit 0
    fi

    # Check for restart signal
    if [ -f "$RESTART_SIGNAL" ]; then
        echo "[Watchdog] RESTART signal detected!"
        rm -f "$RESTART_SIGNAL"
        stop_friday
        sleep 2
        start_friday
    fi

    # Check if Friday process died unexpectedly
    if [ -n "$FRIDAY_PID" ] && ! kill -0 "$FRIDAY_PID" 2>/dev/null; then
        echo "[Watchdog] F.R.I.D.A.Y. process died! Auto-restarting in 5 seconds..."
        sleep 5
        start_friday
    fi

    sleep 3
done
WATCHDOG
chmod +x "$FRIDAY_HOME/friday-watchdog.sh"
ok "Watchdog script created."

# Create systemd service
SYSTEMD_SERVICE="/etc/systemd/system/friday.service"
sudo tee "$SYSTEMD_SERVICE" > /dev/null << SYSDSVC
[Unit]
Description=F.R.I.D.A.Y. Autonomous AI Agent
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=$CURRENT_USER
Environment=HOME=$HOME
Environment=FRIDAY_HOME=$FRIDAY_HOME
Environment=DISPLAY=:0
Environment=XAUTHORITY=$HOME/.Xauthority
WorkingDirectory=$FRIDAY_HOME
ExecStart=$FRIDAY_HOME/friday-watchdog.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SYSDSVC

sudo systemctl daemon-reload
sudo systemctl enable friday.service
ok "friday.service installed and enabled (starts on boot)."

# Midnight Protocol cron job
CRON_CMD="0 0 * * * cd $FRIDAY_HOME && $FRIDAY_HOME/.venv/bin/python -c \"from friday_engine.backup.midnight import MidnightProtocol; from friday_engine.config import load_config; m = MidnightProtocol(load_config().midnight_protocol); from friday_engine.memory.memory_engine import PersistentMemoryEngine; mem = PersistentMemoryEngine(); m.execute_backup(mem)\""
(crontab -l 2>/dev/null | grep -v "MidnightProtocol"; echo "$CRON_CMD") | crontab -
ok "Midnight Protocol cron job installed (daily at 00:00)."

# Upstream Sync cron job (every 6 hours — auto-merge new upstream features)
SYNC_CMD="0 */6 * * * cd $FRIDAY_HOME && $FRIDAY_HOME/.venv/bin/python friday-upstream-sync.py --auto-merge >> $FRIDAY_HOME/logs/upstream_sync.log 2>&1"
(crontab -l 2>/dev/null | grep -v "upstream-sync"; echo "$SYNC_CMD") | crontab -
ok "Upstream Sync cron job installed (every 6 hours — auto-merges updates)."

# Human-Like Nightly Introspection & Self-Correction (daily at 02:00 AM)
INTROSPECT_CMD="0 2 * * * cd $FRIDAY_HOME && $FRIDAY_HOME/.venv/bin/python scripts/midnight_introspection.py --run >> $FRIDAY_HOME/logs/introspection.log 2>&1"
(crontab -l 2>/dev/null | grep -v "midnight_introspection"; echo "$INTROSPECT_CMD") | crontab -
ok "Human-Like Nightly Introspection cron job installed (daily at 02:00 AM)."

# ============================================================================
# PHASE 10: Register Global `friday` Command & Initialize
# ============================================================================
log "━━━ PHASE 10/10: Finalizing Installation ━━━"

# Global launcher
sudo tee /usr/local/bin/friday > /dev/null << LAUNCHER
#!/bin/bash
# F.R.I.D.A.Y. Global Launcher
export FRIDAY_HOME="$FRIDAY_HOME"

# Auto-detect display
if [ -n "\${DISPLAY:-}" ]; then
    export XAUTHORITY="\${XAUTHORITY:-\$HOME/.Xauthority}"
    xhost +local: > /dev/null 2>&1 || true
fi

cd "\$FRIDAY_HOME"
source .venv/bin/activate
python friday_cli.py "\$@"
LAUNCHER
sudo chmod +x /usr/local/bin/friday

# Initialize data directories
mkdir -p "$FRIDAY_HOME/data/skills"
mkdir -p "$FRIDAY_HOME/data/models"
mkdir -p "$FRIDAY_HOME/data/forge_sandbox"
mkdir -p "$FRIDAY_HOME/logs"
mkdir -p "$FRIDAY_HOME/workspace"
mkdir -p "$FRIDAY_HOME/child_builds"

# Update MCP config to point to correct Open-WhatsApp path
MCP_CONFIG="$FRIDAY_HOME/data/mcp_servers.json"
cat > "$MCP_CONFIG" << MCPJSON
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "$FRIDAY_HOME"],
      "description": "Local filesystem access"
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"],
      "description": "Persistent memory store"
    },
    "fetch": {
      "command": "npx",
      "args": ["-y", "mcp-server-fetch"],
      "description": "HTTP content fetcher"
    },
    "open-whatsapp": {
      "command": "node",
      "args": ["$OPENWA_DIR/src/mcp-server.js"],
      "description": "WhatsApp automation and messaging"
    }
  }
}
MCPJSON

ok "MCP server configuration updated."

# Seed skills if the seed script exists
if [ -f "$FRIDAY_HOME/scripts/seed_omni_skills.py" ]; then
    log "Seeding skills library..."
    source "$FRIDAY_HOME/.venv/bin/activate"
    python "$FRIDAY_HOME/scripts/seed_omni_skills.py" 2>/dev/null || warn "Skill seeding had issues."
    python "$FRIDAY_HOME/scripts/seed_agency_marketing_skills.py" 2>/dev/null || true
    python "$FRIDAY_HOME/scripts/seed_trading_financial_skills.py" 2>/dev/null || true
    python "$FRIDAY_HOME/scripts/seed_market_intelligence_skills.py" 2>/dev/null || true
    python "$FRIDAY_HOME/scripts/seed_advanced_ecosystem_skills.py" 2>/dev/null || true
    python "$FRIDAY_HOME/scripts/seed_frontier_skills.py" 2>/dev/null || true
    python "$FRIDAY_HOME/scripts/seed_introspection_and_mcp_skills.py" 2>/dev/null || true
    ok "Skills library seeded (109+ production skills)."
fi

# ============================================================================
# COMPLETE
# ============================================================================
echo ""
echo -e "${GREEN}${FRIDAY_BANNER}${RESET}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo -e "${GREEN}  F.R.I.D.A.Y. INSTALLATION COMPLETE!${RESET}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo ""
echo -e "  ${BOLD}Installation Path:${RESET}  $FRIDAY_HOME"
echo -e "  ${BOLD}Python venv:${RESET}        $FRIDAY_HOME/.venv"
echo -e "  ${BOLD}Agentica Browser:${RESET}   $AGENTICA_DIR"
echo -e "  ${BOLD}Open-WhatsApp MCP:${RESET}  $OPENWA_DIR"
echo -e "  ${BOLD}Systemd Service:${RESET}    friday.service (enabled, starts on boot)"
echo -e "  ${BOLD}Watchdog:${RESET}           $FRIDAY_HOME/friday-watchdog.sh"
echo ""
echo -e "  ${CYAN}Commands:${RESET}"
echo -e "    ${BOLD}friday${RESET}              Start the interactive AI engine"
echo -e "    ${BOLD}friday voice${RESET}        Start hands-free voice mode"
echo -e "    ${BOLD}friday hud${RESET}          Launch the desktop holographic HUD"
echo -e "    ${BOLD}friday setup${RESET}        Re-run the configuration wizard"
echo -e "    ${BOLD}friday market${RESET}       5m candle + news surveillance & forecast"
echo -e "    ${BOLD}friday clean-pdfs${RESET}   Delete raw PDFs while keeping structured data"
echo -e "    ${BOLD}friday update${RESET}       Self-update from GitHub"
echo -e "    ${BOLD}friday evolve${RESET}       Generate a flawless Child Version"
echo -e "    ${BOLD}friday sync${RESET}         Auto-merge new upstream features"
echo -e "    ${BOLD}friday scan${RESET}         Scan the AI landscape for new frameworks"
echo -e "    ${BOLD}friday help${RESET}         Show all commands"
echo ""
echo -e "  ${CYAN}Service Management:${RESET}"
echo -e "    ${BOLD}sudo systemctl start friday${RESET}     Start as background service"
echo -e "    ${BOLD}sudo systemctl stop friday${RESET}      Stop the service"
echo -e "    ${BOLD}sudo systemctl status friday${RESET}    Check status"
echo -e "    ${BOLD}journalctl -u friday -f${RESET}         Live logs"
echo ""
echo -e "  ${YELLOW}Next Steps:${RESET}"
echo -e "    1. Run ${BOLD}friday setup${RESET} to configure your AI model (API keys)"
echo -e "    2. Run ${BOLD}friday${RESET} to start chatting"
echo -e "    3. For auto-start on boot: ${BOLD}sudo systemctl start friday${RESET}"
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
