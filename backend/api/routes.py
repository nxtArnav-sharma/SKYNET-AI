import os
import tempfile
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from backend.agent.brain import brain
from backend.stt.whisper_engine import whisper_engine
from backend.tts.tts_engine import tts_engine
from backend.utils.logger import setup_logger

logger = setup_logger("api_routes")
router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/ask")
async def ask_agent(request: ChatRequest):
    """Text-based interaction with the agent."""
    logger.info(f"Received text request: {request.message}")
    response = await brain.generate_response(request.message)
    return {"response": response}

async def generate_and_return_audio(text: str, headers: dict = None):
    output_path = os.path.join(os.getcwd(), "api_response.mp3")
    await tts_engine.generate_audio_file(text, output_path)
    return FileResponse(path=output_path, media_type="audio/mpeg", filename="response.mp3", headers=headers or {})

from fastapi import WebSocket, WebSocketDisconnect
from backend.utils.ws_manager import ws_manager

@router.websocket("/ws/events")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)

@router.post("/voice")
async def voice_interaction(audio: UploadFile = File(...)):
    """Voice interaction: receive audio, transcribe, validate, get response, generate TTS."""
    print("[SKYNET] Voice received")
    await ws_manager.broadcast({"event": "voice_received"})
    
    try:
        # 1. Receive and save temporary file
        audio_bytes = await audio.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name
        
        # 2. Transcribe with Whisper
        print("[SKYNET] Transcribing audio")
        await ws_manager.broadcast({"event": "transcribing"})
        text = whisper_engine.transcribe_audio_file(tmp_path)
        os.remove(tmp_path) # Clean up temp file
        
        # 3. Validate transcript
        if not text or len(text.strip()) < 2:
            print("[SKYNET] Empty or invalid transcription")
            return await generate_and_return_audio("Boss, I could not detect any speech.")
        
        print(f"[SKYNET] Query received: {text}")
        await ws_manager.broadcast({"event": "thinking", "query": text})
        
        # 4. Get Response from Gemini
        response = await brain.generate_response(text)
        
        if not response:
            return {"status": "stopped"}
        
        # 5. Generate TTS and return
        headers = {}
        if "Global monitoring system" in response or "Opening global intelligence feed" in response:
            headers["X-Tool-Activated"] = "world_monitor"
            
        await ws_manager.broadcast({"event": "speaking"})
        return await generate_and_return_audio(response, headers)
        
    except Exception as e:
        print(f"[SKYNET] Pipeline error: {e}")
        return await generate_and_return_audio("Apologies boss. My neural processing core encountered a malfunction.")

@router.get("/status")
async def system_status():
    """Return status of the SKYNET system."""
    return {
        "status": "online",
        "stt": "faster-whisper",
        "tts": "edge-tts",
        "mcp": "connected"
    }

@router.get("/tools")
async def get_tools():
    """List available MCP tools."""
    return {
        "tools": [
            "open_world_monitor",
            "get_world_news",
            "search_web",
            "fetch_url",
            "open_world_monitor",
            "get_current_time",
            "get_system_info",
            "format_json",
            "word_count"
        ]
    }
