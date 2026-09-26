#!/usr/bin/env bash
# F.R.I.D.A.Y. Watchdog Supervisor
# ─────────────────────────────────
# This is the EXTERNAL supervisor that manages F.R.I.D.A.Y.'s lifecycle.
# F.R.I.D.A.Y. never kills her own process — she signals this watchdog instead.
#
# Signals (touch files):
#   /tmp/friday-restart  → Gracefully restart the F.R.I.D.A.Y. process
#   /tmp/friday-reboot   → Reboot the entire machine (for software installs, etc.)
#
# Auto-recovery:
#   If F.R.I.D.A.Y.'s process dies unexpectedly, watchdog auto-restarts in 5 seconds.
#
# Usage:
#   Managed by systemd (friday.service) — starts automatically on boot.
#   Manual: ./friday-watchdog.sh

set -u

FRIDAY_HOME="${FRIDAY_HOME:-$HOME/F.R.I.D.A.Y}"
VENV="$FRIDAY_HOME/.venv/bin/activate"
LOG_FILE="$FRIDAY_HOME/logs/watchdog.log"
RESTART_SIGNAL="/tmp/friday-restart"
REBOOT_SIGNAL="/tmp/friday-reboot"
FRIDAY_PID=""
RESTART_COUNT=0
MAX_RAPID_RESTARTS=10
RAPID_RESTART_WINDOW=300  # 5 minutes

mkdir -p "$FRIDAY_HOME/logs"

log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] [Watchdog] $1"
    echo "$msg"
    echo "$msg" >> "$LOG_FILE"
}

start_friday() {
    log "Starting F.R.I.D.A.Y. engine..."
    source "$VENV"
    cd "$FRIDAY_HOME"

    # Auto-detect display for GUI
    if [ -n "${DISPLAY:-}" ]; then
        export XAUTHORITY="${XAUTHORITY:-$HOME/.Xauthority}"
        xhost +local: > /dev/null 2>&1 || true
    fi

    python friday_cli.py &
    FRIDAY_PID=$!
    log "F.R.I.D.A.Y. started with PID $FRIDAY_PID"
}

stop_friday() {
    if [ -n "$FRIDAY_PID" ] && kill -0 "$FRIDAY_PID" 2>/dev/null; then
        log "Stopping F.R.I.D.A.Y. (PID $FRIDAY_PID)..."
        kill -TERM "$FRIDAY_PID" 2>/dev/null
        # Wait up to 15 seconds for graceful shutdown
        local count=0
        while kill -0 "$FRIDAY_PID" 2>/dev/null && [ $count -lt 15 ]; do
            sleep 1
            count=$((count + 1))
        done
        # Force kill if still running
        if kill -0 "$FRIDAY_PID" 2>/dev/null; then
            log "Force killing F.R.I.D.A.Y. (PID $FRIDAY_PID)..."
            kill -9 "$FRIDAY_PID" 2>/dev/null
        fi
        wait "$FRIDAY_PID" 2>/dev/null || true
    fi
    FRIDAY_PID=""
}

cleanup() {
    log "Watchdog shutting down..."
    stop_friday
    rm -f "$RESTART_SIGNAL" "$REBOOT_SIGNAL"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Clean any stale signals from previous runs
rm -f "$RESTART_SIGNAL" "$REBOOT_SIGNAL"

log "═══════════════════════════════════════════════════"
log "  F.R.I.D.A.Y. Watchdog Supervisor — ONLINE"
log "  FRIDAY_HOME: $FRIDAY_HOME"
log "═══════════════════════════════════════════════════"

# Initial start
start_friday

LAST_RESTART_TIME=$(date +%s)

# Main supervisor loop
while true; do
    # Check for REBOOT signal
    if [ -f "$REBOOT_SIGNAL" ]; then
        log "⚡ REBOOT signal detected!"
        rm -f "$REBOOT_SIGNAL" "$RESTART_SIGNAL"
        stop_friday
        log "Rebooting system in 3 seconds..."
        sleep 3
        sudo reboot
        exit 0
    fi

    # Check for RESTART signal
    if [ -f "$RESTART_SIGNAL" ]; then
        log "🔄 RESTART signal detected!"
        rm -f "$RESTART_SIGNAL"
        stop_friday
        sleep 2
        start_friday
        RESTART_COUNT=$((RESTART_COUNT + 1))
        LAST_RESTART_TIME=$(date +%s)
    fi

    # Check if Friday process died unexpectedly
    if [ -n "$FRIDAY_PID" ] && ! kill -0 "$FRIDAY_PID" 2>/dev/null; then
        log "💀 F.R.I.D.A.Y. process died unexpectedly!"

        # Check for crash loop (too many restarts in a short window)
        CURRENT_TIME=$(date +%s)
        TIME_DIFF=$((CURRENT_TIME - LAST_RESTART_TIME))

        if [ $TIME_DIFF -lt $RAPID_RESTART_WINDOW ] && [ $RESTART_COUNT -ge $MAX_RAPID_RESTARTS ]; then
            log "❌ CRASH LOOP DETECTED ($RESTART_COUNT restarts in ${TIME_DIFF}s). Entering cooldown for 60 seconds..."
            sleep 60
            RESTART_COUNT=0
        fi

        log "Auto-restarting in 5 seconds..."
        sleep 5
        start_friday
        RESTART_COUNT=$((RESTART_COUNT + 1))
        LAST_RESTART_TIME=$CURRENT_TIME

        # Reset counter if outside rapid window
        if [ $TIME_DIFF -ge $RAPID_RESTART_WINDOW ]; then
            RESTART_COUNT=1
        fi
    fi

    sleep 3
done
