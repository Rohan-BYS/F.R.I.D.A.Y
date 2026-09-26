#!/usr/bin/env bash
# ==============================================================================
# F.R.I.D.A.Y. Midnight Protocol - Linux Cron / Systemd Trigger
# Runs nightly at 00:00 to push state and knowledge to remote repository
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

cd "${PROJECT_ROOT}"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Triggering F.R.I.D.A.Y. Midnight Protocol..."

# Run the python backup module directly
if command -v python3 &>/dev/null; then
    python3 -c "from friday_engine.backup.midnight import MidnightProtocol; p = MidnightProtocol(); print(p.execute_backup())"
elif command -v python &>/dev/null; then
    python -c "from friday_engine.backup.midnight import MidnightProtocol; p = MidnightProtocol(); print(p.execute_backup())"
else
    # Fallback to direct git
    git add -A
    git commit -m "Nightly auto-backup [Midnight Protocol] $(date +%F)" || true
    git push origin main || echo "Git push skipped or remote not reachable"
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Midnight Protocol execution finished."
