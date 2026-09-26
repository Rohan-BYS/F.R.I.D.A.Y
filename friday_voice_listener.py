"""
F.R.I.D.A.Y. Voice Listener (Jarvis Audio Loop).
Run this script to enable hands-free voice interaction.
"""

import asyncio
import os
import sys

# Ensure friday_engine is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from friday_engine.core.engine import FridayEngine
from friday_engine.config import FridayConfig

async def main():
    print("Initializing F.R.I.D.A.Y. Core Engine...")
    config = FridayConfig()
    engine = FridayEngine(config)
    await engine.boot()

    print("\n" + "="*50)
    print("F.R.I.D.A.Y. VOICE LOOP ACTIVE")
    print("Speak into your microphone. Say 'exit' to stop.")
    print("="*50 + "\n")

    if not hasattr(engine, 'hearing') or not engine.hearing.recognizer:
        print("[Error] Hearing Engine is not available. Please pip install SpeechRecognition faster-whisper.")
        return

    # Preload local Whisper model to avoid delay during conversation
    engine.hearing.load_whisper()
    
    # Say hello
    engine.speech.speak("F.R.I.D.A.Y. is online and listening.")

    while True:
        try:
            print("Listening for wake word or command...")
            user_speech = engine.hearing.listen(timeout=5)
            
            if user_speech:
                print(f"You said: {user_speech}")
                
                if "exit" in user_speech.lower() or "shutdown" in user_speech.lower():
                    engine.speech.speak("Shutting down voice listener.")
                    break
                    
                # Route to engine
                print("Processing...")
                response_text = await engine.chat(user_speech)
                print(f"Friday: {response_text}")
                
                # Speak response
                engine.speech.speak(response_text)
                
        except KeyboardInterrupt:
            print("\nShutting down...")
            break
        except Exception as e:
            print(f"Error in voice loop: {e}")

if __name__ == "__main__":
    asyncio.run(main())
