import os
import asyncio
import numpy as np
import sounddevice as sd
import re
import wave
import time
from kokoro_onnx import Kokoro
from backend.utils.logger import setup_logger
from backend.config.settings import settings
import backend.utils.state as global_state

logger = setup_logger("tts_engine")

class TTSEngine:
    def __init__(self):
        self.model_path = os.path.join(os.getcwd(), "backend", "models", "kokoro", "kokoro-v1.0.onnx")
        self.voices_path = os.path.join(os.getcwd(), "backend", "models", "kokoro", "voices-v1.0.bin")
        self.default_voice = "af_bella"
        self.lang_code = "en-us"
        self.speed = 0.95
        self.output_wav = os.path.join(os.getcwd(), "output.wav")
        self.is_speaking = False
        
        # Initialize Kokoro
        logger.info("Initializing Kokoro-ONNX TTS Engine...")
        try:
            if not os.path.exists(self.model_path) or not os.path.exists(self.voices_path):
                logger.warning(f"Kokoro model files not found. TTS disabled.")
                self.kokoro = None
            else:
                self.kokoro = Kokoro(self.model_path, self.voices_path)
                logger.info("Kokoro-ONNX TTS Engine initialized.")
        except Exception as e:
            logger.error(f"Failed to initialize Kokoro-ONNX: {e}")
            self.kokoro = None

    def _add_natural_pauses(self, text: str) -> str:
        """Inject breathing pauses at punctuation marks."""
        text = text.replace(",", ", [pause]")
        text = text.replace(".", ". [pause_long]")
        text = text.replace("?", "? [pause_long]")
        text = text.replace(":", ": [pause]")
        text = text.replace(";", "; [pause]")
        return text

    def _add_emphasis(self, text: str) -> str:
        """Automatically wrap critical keywords in emphasis tags."""
        keywords = ["important", "critical", "warning", "significant", "alert", "danger", "immediately"]
        for word in keywords:
            text = re.sub(
                rf"\b({word})\b",
                r"[emph]\1[/emph]",
                text,
                flags=re.IGNORECASE
            )
        return text

    def _parse_markup(self, text: str):
        """Parse custom SSML-like markup into tokens."""
        tokens = []
        pattern = r'(\[pause(?:_long)?\]|\[emph\].*?\[/emph\]|\[slow\].*?\[/slow\]|\[fast\].*?\[/fast\])'
        parts = re.split(pattern, text)

        for part in parts:
            if not part: continue

            if part == "[pause]":
                tokens.append({"type": "pause", "duration": 0.3})
            elif part == "[pause_long]":
                tokens.append({"type": "pause", "duration": 0.7})
            elif part.startswith("[emph]"):
                content = re.sub(r'\[/?emph\]', '', part)
                tokens.append({"type": "speech", "text": content, "mode": "emph"})
            elif part.startswith("[slow]"):
                content = re.sub(r'\[/?slow\]', '', part)
                tokens.append({"type": "speech", "text": content, "mode": "slow"})
            elif part.startswith("[fast]"):
                content = re.sub(r'\[/?fast\]', '', part)
                tokens.append({"type": "speech", "text": content, "mode": "fast"})
            else:
                tokens.append({"type": "speech", "text": part, "mode": "normal"})
        return tokens

    def _get_voice_config(self, mode: str, base_speed: float):
        """Map delivery mode to voice speed."""
        if mode == "emph":
            return {"speed": base_speed * 1.1} # Higher intensity
        elif mode == "slow":
            return {"speed": base_speed * 0.85}
        elif mode == "fast":
            return {"speed": base_speed * 1.15}
        return {"speed": base_speed}

    async def speak(self, text: str, voice: str = None, speed: float = None) -> str:
        """Converts text to speech with natural pacing, emphasis, and interrupts."""
        if self.is_speaking:
            logger.warning("TTS is already speaking. Skipping request.")
            return self.output_wav

        self.is_speaking = True
        try:
            global_state.stop_speaking = False
            if not self.kokoro: return ""

            # 1. Pre-process text
            text = self._add_emphasis(text)
            text = self._add_natural_pauses(text)
            
            # 2. Parse markup into tokens
            tokens = self._parse_markup(text)
            
            current_voice = voice or self.default_voice
            base_speed = speed or self.speed
            all_audio = []
            sample_rate = 24000

            for token in tokens:
                if global_state.stop_speaking:
                    sd.stop()
                    break

                if token["type"] == "pause":
                    await asyncio.sleep(token["duration"])
                    continue

                # Speech Token
                config = self._get_voice_config(token["mode"], base_speed)
                try:
                    samples, sr = self.kokoro.create(
                        token["text"], 
                        voice=current_voice, 
                        speed=config["speed"], 
                        lang=self.lang_code
                    )
                    sample_rate = sr
                    all_audio.append(samples)
                    
                    sd.play(samples, sr)
                    
                    duration = len(samples) / sr
                    steps = int(duration / 0.1)
                    for _ in range(steps):
                        if global_state.stop_speaking:
                            sd.stop()
                            return self.output_wav
                        await asyncio.sleep(0.1)
                except Exception as e:
                    logger.error(f"TTS Token Error: {e}")
                    continue

            # Save full audio to WAV
            if all_audio:
                combined = np.concatenate(all_audio)
                with wave.open(self.output_wav, "wb") as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(sample_rate)
                    wf.writeframes((combined * 32767).astype(np.int16).tobytes())
                
        except Exception as e:
            logger.error(f"Error during TTS process: {e}")
        finally:
            sd.stop()
            self.is_speaking = False
        return self.output_wav

    def stop_audio(self):
        global_state.stop_speaking = True
        sd.stop()
        logger.info("Audio stop command issued.")

# Instantiate
tts_engine = TTSEngine()

async def speak(text: str, voice: str = None, speed: float = None):
    return await tts_engine.speak(text, voice, speed)

def stop_audio():
    tts_engine.stop_audio()
