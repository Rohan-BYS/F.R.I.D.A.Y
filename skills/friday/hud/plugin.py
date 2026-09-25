import os
import subprocess
import json

HUD_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(HUD_DIR, ".friday_state.json")

def hud_start() -> str:
    """Launches the PyQt6 Desktop Overlay."""
    script_path = os.path.join(HUD_DIR, "hud_ui.py")
    if not os.path.exists(script_path):
        return "Error: hud_ui.py not found."
    
    # Launch in background, detaching from current process
    subprocess.Popen(
        ["python3", script_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True
    )
    return "F.R.I.D.A.Y. HUD (Orb) launched successfully on desktop."

def hud_set_state(status: str, message: str) -> str:
    """Updates the F.R.I.D.A.Y. HUD orb color, animation, and display text.
    Valid statuses: idle, listening, thinking, speaking.
    """
    valid_statuses = ["idle", "listening", "thinking", "speaking"]
    if status not in valid_statuses:
        status = "idle"
        
    try:
        with open(STATE_FILE, "w") as f:
            json.dump({"status": status, "message": message}, f)
        return f"HUD state updated to {status}: '{message}'."
    except Exception as e:
        return f"Failed to update HUD state: {str(e)}"
