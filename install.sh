#!/bin/bash
set -e

echo "========================================================="
echo "       F.R.I.D.A.Y. NATIVE OMNI-CORE DEPLOYMENT"
echo "========================================================="

echo "[1/5] Installing Host OS Dependencies..."
sudo apt-get update -y
sudo apt-get install -y git curl python3-pip python3-venv \
    xvfb libgl1 libglib2.0-0 portaudio19-dev alsa-utils \
    libdbus-1-3 x11-utils docker.io \
    libxcb-xinerama0 libxkbcommon-x11-0 \
    python3-tk xdotool wmctrl scrot

# Install Node.js for WhatsApp MCP
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Enable Docker (F.R.I.D.A.Y. uses this to sandbox untrusted code)
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $USER

TARGET_DIR="$HOME/F.R.I.D.A.Y"
if [ -d "$TARGET_DIR" ]; then
    echo "Directory '$TARGET_DIR' already exists. Updating..."
    cd "$TARGET_DIR"
    git pull
else
    echo "[2/5] Cloning F.R.I.D.A.Y. Repository..."
    git clone https://github.com/Rohan-BYS/F.R.I.D.A.Y.git "$TARGET_DIR"
    cd "$TARGET_DIR"
fi

echo "[3/5] Initializing Native Python Environment..."
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install pyaudio || echo "[WARN] pyaudio failed. Voice mic input may not work."
pip install PyQt6 sounddevice numpy
playwright install --with-deps chromium

echo "[4/5] Registering 'friday' command globally..."
sudo tee /usr/local/bin/friday > /dev/null << 'LAUNCHER'
#!/bin/bash
# F.R.I.D.A.Y. Global Launcher
# Auto-detect display for GUI capabilities
if [ -n "$DISPLAY" ]; then
    # Fix X auth when launched from different terminal sessions
    export XAUTHORITY="${XAUTHORITY:-$HOME/.Xauthority}"
    # Allow local connections to X server
    xhost +local: > /dev/null 2>&1 || true
fi

cd "$HOME/F.R.I.D.A.Y"
source .venv/bin/activate
python friday_cli.py "$@"
LAUNCHER
sudo chmod +x /usr/local/bin/friday

echo "[5/5] Done!"
echo "========================================================="
echo "F.R.I.D.A.Y. is now fully installed on your system!"
echo ""
echo "Commands:"
echo "  friday          - Start the AI engine"
echo "  friday update   - Self-update from GitHub"
echo "  friday hud      - Launch the desktop visualizer"
echo "  friday help     - Show all commands"
echo "========================================================="
