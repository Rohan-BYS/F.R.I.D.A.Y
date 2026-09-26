"""
F.R.I.D.A.Y. OS-Level GUI Control (Ghost in the Machine).
Cross-platform native OS automation for Windows, Mac, and Linux.
"""

import os
import base64
import time
from typing import Dict, Optional, Tuple, Any
from friday_engine.logger import logger

try:
    import pyautogui
    # Fail-safes are critical for AGI controlling a mouse
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.5
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False


class ComputerController:
    """
    Takes control of the host operating system's mouse and keyboard.
    Fully cross-platform (Windows, macOS, Linux).
    """
    def __init__(self):
        self.enabled = GUI_AVAILABLE

    def get_screen_size(self) -> Tuple[int, int]:
        if not self.enabled: return (0, 0)
        return pyautogui.size()

    def screenshot(self, return_base64: bool = True) -> Optional[str]:
        """Capture the entire screen, cross-platform."""
        if not self.enabled:
            logger.error("PyAutoGUI not installed. Cannot take OS screenshot.")
            return None
        
        import io
        try:
            image = pyautogui.screenshot()
            if not return_base64:
                return image
                
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            return base64.b64encode(buffered.getvalue()).decode("utf-8")
        except Exception as e:
            logger.error(f"Failed to capture OS screen: {e}")
            return None

    def move_mouse(self, x: int, y: int, duration: float = 0.5):
        """Move the physical mouse cross-platform."""
        if not self.enabled: return
        try:
            pyautogui.moveTo(x, y, duration=duration, tween=pyautogui.easeInOutQuad)
            logger.debug(f"Moved mouse to ({x}, {y})")
        except pyautogui.FailSafeException:
            logger.warning("Mouse movement triggered fail-safe (corner of screen).")

    def click(self, x: Optional[int] = None, y: Optional[int] = None, button: str = "left", clicks: int = 1):
        """Click the physical mouse."""
        if not self.enabled: return
        try:
            pyautogui.click(x=x, y=y, clicks=clicks, button=button)
            logger.debug(f"Clicked {button} button {clicks} times at ({x}, {y})")
        except Exception as e:
            logger.error(f"Mouse click failed: {e}")

    def type_text(self, text: str, interval: float = 0.05):
        """Type text via native OS keyboard events."""
        if not self.enabled: return
        try:
            pyautogui.write(text, interval=interval)
            logger.debug(f"Typed text: {text[:20]}...")
        except Exception as e:
            logger.error(f"Keyboard typing failed: {e}")

    def press_key(self, key: str, modifiers: Optional[list[str]] = None):
        """Press a key or a combination (e.g., ctrl+c)."""
        if not self.enabled: return
        try:
            if modifiers:
                pyautogui.hotkey(*modifiers, key)
            else:
                pyautogui.press(key)
        except Exception as e:
            logger.error(f"Key press failed: {e}")
