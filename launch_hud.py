import os
import sys

# Ensure the parent directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from friday_engine.gui.hud import launch_hud

if __name__ == "__main__":
    print("Launching F.R.I.D.A.Y. HUD...")
    launch_hud()
