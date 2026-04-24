import asyncio
import os
import pygame
from backend.utils.logger import setup_logger
from backend.stt.whisper_engine import whisper_engine
from backend.tts.tts_engine import tts_engine
from backend.agent.brain import brain

logger = setup_logger("voice_agent")

class VoiceAgent:
    def __init__(self):
        self.is_running = False
        pygame.mixer.init()

    async def play_audio(self, file_path: str):
        """Play audio file locally using pygame."""
        import backend.utils.state as global_state
        global_state.stop_speaking = False
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                if global_state.stop_speaking:
                    pygame.mixer.music.stop()
                    logger.info("Playback interrupted by user.")
                    break
                await asyncio.sleep(0.1)
            pygame.mixer.music.unload()
        except Exception as e:
            logger.error(f"Error playing audio: {e}")

    async def run_loop(self):
        """Main AI loop: Record -> STT -> Brain -> TTS -> Play"""
        self.is_running = True
        logger.info("Voice Agent loop started.")
        
        while self.is_running:
            try:
                # 1. Listen and Transcribe
                text = whisper_engine.record_and_transcribe(duration=5)
                
                if not text or len(text.strip()) < 2:
                    logger.info("No speech detected.")
                    continue
                
                # 2. Brain processing
                logger.info(f"User: {text}")
                response = await brain.generate_response(text)
                logger.info(f"Agent: {response}")
                
                # 3. TTS
                output_path = os.path.join(os.getcwd(), "response.mp3")
                await tts_engine.generate_audio_file(response, output_path)
                
                # 4. Play audio
                await self.play_audio(output_path)
                
            except KeyboardInterrupt:
                self.is_running = False
                logger.info("Voice Agent stopped by user.")
            except Exception as e:
                logger.error(f"Error in voice loop: {e}")
                await asyncio.sleep(1)

    def stop(self):
        self.is_running = False

voice_agent = VoiceAgent()

if __name__ == "__main__":
    asyncio.run(voice_agent.run_loop())
