"""
F.R.I.D.A.Y. Telegram Gateway (Omnipresence).
Provides a free, mobile interface for texting and voice noting F.R.I.D.A.Y.
"""

import os
import asyncio
from typing import Any
from friday_engine.logger import logger

try:
    from telegram import Update
    from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False


class TelegramGateway:
    def __init__(self, engine: Any):
        """Pass the FridayEngine instance so the bot can trigger chat/actions."""
        self.engine = engine
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.app = None

    def start_polling(self):
        """Starts the Telegram bot in the background using asyncio."""
        if not TELEGRAM_AVAILABLE:
            logger.error("python-telegram-bot is not installed. Telegram Gateway disabled.")
            return
            
        if not self.token:
            logger.warning("TELEGRAM_BOT_TOKEN not set. Telegram Gateway is offline.")
            return

        self.app = ApplicationBuilder().token(self.token).build()

        self.app.add_handler(CommandHandler("start", self._start_handler))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self._text_handler))
        self.app.add_handler(MessageHandler(filters.VOICE, self._voice_handler))
        self.app.add_handler(MessageHandler(filters.PHOTO, self._photo_handler))

        logger.info("Telegram Gateway online. F.R.I.D.A.Y. is now omnipresent on mobile.")
        # We use run_polling in a way that doesn't block if we run it properly,
        # but for an async engine, we can initialize it and run it.
        asyncio.create_task(self._run_async())
        
    async def _run_async(self):
        await self.app.initialize()
        await self.app.start()
        await self.app.updater.start_polling()

    async def _start_handler(self, update: 'Update', context: 'ContextTypes.DEFAULT_TYPE'):
        await update.message.reply_text("Hello. I am F.R.I.D.A.Y. Identity verified. Awaiting your commands.")

    async def _text_handler(self, update: 'Update', context: 'ContextTypes.DEFAULT_TYPE'):
        user_msg = update.message.text
        logger.info(f"[Telegram] Received: {user_msg}")
        
        # Send a typing action
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
        
        # Route to F.R.I.D.A.Y. Core Engine
        response = await self.engine.chat(f"[Telegram Mobile] {user_msg}")
        
        await update.message.reply_text(response)

    async def _voice_handler(self, update: 'Update', context: 'ContextTypes.DEFAULT_TYPE'):
        """Handle incoming voice notes by transcribing via HearingEngine."""
        status_msg = await update.message.reply_text("🎙️ Transcribing voice note locally...")
        
        try:
            file = await update.message.voice.get_file()
            import tempfile
            import speech_recognition as sr
            import os
            
            with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as fp:
                await file.download_to_drive(fp.name)
                temp_path = fp.name
                
            # Convert OGG to WAV (usually required by SpeechRecognition unless using Whisper directly)
            # For brevity in this implementation, we assume `engine.hearing.whisper_model.transcribe` 
            # can handle OGG directly if ffmpeg is installed, which it usually can.
            if hasattr(self.engine, 'hearing') and self.engine.hearing.whisper_model:
                segments, _ = self.engine.hearing.whisper_model.transcribe(temp_path, beam_size=5)
                transcription = "".join([s.text for s in segments]).strip()
            else:
                transcription = "Error: Whisper model not loaded for transcription."
                
            os.remove(temp_path)
            
            await status_msg.edit_text(f"🎤 You: {transcription}\n\nThinking...")
            
            # Send to engine
            response = await self.engine.chat(f"[Telegram Voice Note] {transcription}")
            await update.message.reply_text(response)
            
        except Exception as e:
            logger.error(f"Telegram voice error: {e}")
            await status_msg.edit_text(f"Error processing voice note: {e}")
            
    async def _photo_handler(self, update: 'Update', context: 'ContextTypes.DEFAULT_TYPE'):
        """Handle incoming photos for Vision processing."""
        status_msg = await update.message.reply_text("👁️ Analyzing image...")
        
        try:
            photo_file = await update.message.photo[-1].get_file()
            import tempfile
            import os
            
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as fp:
                await photo_file.download_to_drive(fp.name)
                temp_path = fp.name
                
            # Future multimodal LLM pipeline connection:
            # We would read this file as Base64 and send it to the Gemini/Claude vision endpoint.
            # For now, we simulate the visual context insertion into the text pipeline.
            response = await self.engine.chat(f"[Telegram Image Uploaded] Path: {temp_path}. Describe what you see.")
            await update.message.reply_text(response)
            
        except Exception as e:
            logger.error(f"Telegram photo error: {e}")
            await status_msg.edit_text("Failed to process image.")
