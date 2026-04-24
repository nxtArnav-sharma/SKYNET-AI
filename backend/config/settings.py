import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    # LLM Settings
    LLM_PROVIDER: str = "gemini"
    GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

    # STT & TTS
    TTS_VOICE: str = "en-US-SteffanNeural" # Default edge-tts voice
    WHISPER_MODEL: str = "tiny.en" # Fast model for local inference

    # App Settings
    MCP_SERVER_PORT: int = 8000
    API_PORT: int = 8001
    
    # Paths
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

settings = Settings()
