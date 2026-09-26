"""
F.R.I.D.A.Y. Speech Module (Mouth).
Uses edge-tts for high-quality, free Neural Text-to-Speech, with pyttsx3 as an offline fallback.
"""

import asyncio
import os
import tempfile
import threading
from typing import Optional

try:
    import edge_tts
    EDGE_AVAILABLE = True
except ImportError:
    EDGE_AVAILABLE = False

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False


class SpeechEngine:
    def __init__(self, voice: str = "en-US-JennyNeural"):
        self.voice = voice
        self.offline_engine = pyttsx3.init() if PYTTSX3_AVAILABLE else None
        if self.offline_engine:
            # Try to set a female voice for F.R.I.D.A.Y.
            voices = self.offline_engine.getProperty('voices')
            for v in voices:
                if "Zira" in v.name or "Female" in v.name:
                    self.offline_engine.setProperty('voice', v.id)
                    break
        
    async def speak_async(self, text: str):
        """Asynchronously speak text using Edge TTS (high quality) or fallback."""
        if not text.strip():
            return
            
        if EDGE_AVAILABLE:
            try:
                communicate = edge_tts.Communicate(text, self.voice)
                
                # We need to play the audio. We'll save to a temp file and play it.
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                    temp_path = fp.name
                    
                await communicate.save(temp_path)
                
                # Play audio across platforms
                if os.name == 'nt':  # Windows
                    os.system(f"start /min mplay32 /play /close {temp_path}")
                else:  # Mac/Linux
                    os.system(f"mpg123 -q {temp_path} || afplay {temp_path}")
                return
            except Exception as e:
                print(f"[Speech] Edge-TTS failed, falling back to offline: {e}")
                
        self.speak_offline(text)
        
    def speak_offline(self, text: str):
        """Offline fallback using pyttsx3."""
        if not PYTTSX3_AVAILABLE or not self.offline_engine:
            print(f"[Speech disabled] F.R.I.D.A.Y: {text}")
            return
            
        def _speak():
            self.offline_engine.say(text)
            self.offline_engine.runAndWait()
            
        # Run in a thread so it doesn't block the async loop
        threading.Thread(target=_speak, daemon=True).start()

    def speak(self, text: str):
        """Synchronous wrapper for speaking."""
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(self.speak_async(text))
        except RuntimeError:
            asyncio.run(self.speak_async(text))
