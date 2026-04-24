# SKYNET AI Platform

A fully local AI assistant platform featuring voice interaction, local TTS/STT, reasoning, and a modern cyberpunk dashboard.

## Features
- **Local STT**: `faster-whisper`
- **Local TTS**: `edge-tts`
- **Local Tool execution**: FastMCP architecture
- **Web UI**: Next.js & TailwindCSS (Cyberpunk SKYNET theme)
- **API Backend**: FastAPI
- **LLM Reasoning Engine**: Powered by Google Gemini

## Setup

1. Create a virtual environment and install dependencies:
```bash
python -m venv .venv
source .venv/Scripts/activate # Windows
pip install -r requirements.txt
```

2. Set up `.env` file with `GEMINI_API_KEY`.

3. Install frontend dependencies:
```bash
cd frontend
npm install
```

## Running the Platform
```bash
python run_skynet.py
```
