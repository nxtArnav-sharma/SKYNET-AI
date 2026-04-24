# SKYNET AUTO INSTALLER

# Developer: Arnav Sharma

Write-Host ""
Write-Host "====================================="
Write-Host "      SKYNET AI INSTALLER v1.0"
Write-Host "====================================="
Write-Host ""

# -------------------------------

# Check Python

# -------------------------------

Write-Host "Checking Python installation..."

$python = Get-Command python -ErrorAction SilentlyContinue

if (!$python) {
    Write-Host "Python not found. Please install Python 3.11."
    exit
}

python --version

# -------------------------------

# Create Virtual Environment

# -------------------------------

Write-Host ""
Write-Host "Creating Python virtual environment..."

python -m venv .venv

Write-Host "Activating environment..."

& "..venv\Scripts\Activate.ps1"

# -------------------------------

# Upgrade pip

# -------------------------------

Write-Host ""
Write-Host "Upgrading pip..."

python -m pip install --upgrade pip

# -------------------------------

# Install Backend Dependencies

# -------------------------------

Write-Host ""
Write-Host "Installing backend dependencies..."

pip install fastapi
pip install uvicorn
pip install mcp
pip install python-dotenv
pip install websockets
pip install httpx
pip install numpy
pip install sounddevice
pip install faster-whisper
pip install edge-tts
pip install orjson
pip install uvloop

# -------------------------------

# Install AI extras

# -------------------------------

Write-Host ""
Write-Host "Installing optional AI tools..."

pip install google-generativeai
pip install sentence-transformers
pip install chromadb

# -------------------------------

# Install Frontend

# -------------------------------

Write-Host ""
Write-Host "Installing frontend dependencies..."

Set-Location frontend

npm install

Set-Location ..

# -------------------------------

# Create Environment File

# -------------------------------

Write-Host ""
Write-Host "Creating .env configuration..."

$envContent = @"
GEMINI_API_KEY=your_key_here
SKYNET_MODE=development
"@

Set-Content ".env" $envContent

# -------------------------------

# Installation Complete

# -------------------------------

Write-Host ""
Write-Host "====================================="
Write-Host " SKYNET INSTALLATION COMPLETE "
Write-Host "====================================="
Write-Host ""

Write-Host "Starting SKYNET..."

python run_skynet.py
