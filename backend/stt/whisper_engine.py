import os
import numpy as np
from faster_whisper import WhisperModel
import sounddevice as sd
from backend.utils.logger import setup_logger

logger = setup_logger("whisper_engine")

class WhisperEngine:
    def __init__(self, model_size="tiny.en"):
        logger.info(f"Loading Whisper model {model_size}...")
        self.model = WhisperModel(model_size, device="cpu", compute_type="int8")
        self.sample_rate = 16000
        logger.info("Whisper model loaded.")

    def transcribe_audio_file(self, audio_path: str) -> str:
        """Transcribe an audio file."""
        segments, _ = self.model.transcribe(audio_path, beam_size=5)
        text = " ".join([segment.text for segment in segments])
        return text.strip()

    def transcribe_audio_bytes(self, audio_data: bytes) -> str:
        """Transcribe raw audio bytes. (Requires conversion to numpy array)"""
        # Convert bytes to numpy array of float32
        audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
        segments, _ = self.model.transcribe(audio_np, beam_size=5)
        text = " ".join([segment.text for segment in segments])
        return text.strip()

    def record_and_transcribe(self, duration: int = 5) -> str:
        """Record audio from the local microphone and transcribe it."""
        logger.info(f"Recording for {duration} seconds...")
        audio_data = sd.rec(int(duration * self.sample_rate), samplerate=self.sample_rate, channels=1, dtype='int16')
        sd.wait()
        logger.info("Recording complete. Transcribing...")
        
        audio_np = audio_data.flatten().astype(np.float32) / 32768.0
        segments, _ = self.model.transcribe(audio_np, beam_size=5)
        text = " ".join([segment.text for segment in segments])
        logger.info(f"Transcription: {text}")
        return text.strip()

whisper_engine = WhisperEngine()
