"""
F.R.I.D.A.Y. Hearing Module (Ears).
Uses faster-whisper for free, local, accurate Speech-to-Text transcription.
"""

import asyncio
from typing import Optional
from friday_engine.logger import logger

try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False


class HearingEngine:
    def __init__(self, wake_word: str = "friday"):
        self.wake_word = wake_word.lower()
        self.recognizer = sr.Recognizer() if SR_AVAILABLE else None
        
        # We could load faster-whisper here if installed
        self.whisper_model = None

    def load_whisper(self):
        try:
            from faster_whisper import WhisperModel
            logger.info("Loading local Whisper model (this may take a moment)...")
            self.whisper_model = WhisperModel("base.en", device="cpu", compute_type="int8")
            logger.info("Whisper model loaded.")
        except ImportError:
            logger.warning("faster-whisper not installed. Falling back to basic recognizer.")

    def listen(self, timeout: int = 5) -> Optional[str]:
        """Listen to microphone and return transcribed text."""
        if not self.recognizer:
            logger.error("SpeechRecognition library not installed.")
            return None
            
        with sr.Microphone() as source:
            logger.info("Adjusting for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            logger.info("Listening...")
            try:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
            except sr.WaitTimeoutError:
                return None
                
        # Transcribe
        return self.transcribe(audio)
        
    def transcribe(self, audio_data: 'sr.AudioData') -> Optional[str]:
        """Transcribe audio data using the best available local model."""
        if self.whisper_model:
            import tempfile
            import os
            
            # Save audio to temp wav file for Whisper
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as fp:
                fp.write(audio_data.get_wav_data())
                temp_path = fp.name
                
            try:
                segments, _ = self.whisper_model.transcribe(temp_path, beam_size=5)
                text = "".join([segment.text for segment in segments]).strip()
                return text
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
        else:
            # Fallback to Google's free online recognizer built into speech_recognition
            try:
                text = self.recognizer.recognize_google(audio_data)
                return text
            except sr.UnknownValueError:
                return None
            except sr.RequestError as e:
                logger.error(f"Google Speech Recognition error: {e}")
                return None
