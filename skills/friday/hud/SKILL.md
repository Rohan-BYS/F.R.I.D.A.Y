---
name: friday_hud
description: Interface with the F.R.I.D.A.Y. PyQt6 Desktop Holographic UI (Orb).
category: system
---

# F.R.I.D.A.Y. HUD (Orb Interface)

## Overview
This skill allows F.R.I.D.A.Y. to spawn, manage, and update the visual state of the floating desktop UI Orb.

## Capabilities
1. `hud_start()`: Launches the `hud_ui.py` PyQt6 overlay in a detached background process.
2. `hud_set_state(status: str, message: str)`: Updates the orb's color and status text. Valid statuses: `idle`, `listening`, `thinking`, `speaking`.

## Usage Guidelines
- The HUD is a PyQt6 application requiring X11 or Wayland on Linux. 
- Ensure `python3-pyqt6` is installed.
- Do not call `hud_start()` if the container is fully headless without X11 forwarding.
