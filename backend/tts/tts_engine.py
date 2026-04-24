import os
import asyncio
import edge_tts
from backend.utils.logger import setup_logger
from backend.config.settings import settings

logger = setup_logger("tts_engine")

class TTSEngine:
    def __init__(self, voice: str = settings.TTS_VOICE):
        self.voice = voice

    async def generate_audio_file(self, text: str, output_path: str) -> str:
        """Generate an audio file from text and save it to output_path."""
        logger.info(f"Generating audio for text: {text[:50]}...")
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(output_path)
        logger.info(f"Audio saved to {output_path}")
        return output_path

tts_engine = TTSEngine()
