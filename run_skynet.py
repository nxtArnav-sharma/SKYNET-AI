import subprocess
import os
import sys
import time

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def run_mcp():
    print("[SKYNET] Starting MCP Server...")
    return subprocess.Popen(
        [sys.executable, "-m", "backend.mcp.server"],
        cwd=ROOT_DIR
    )

def run_backend():
    print("[SKYNET] Starting FastAPI Backend...")
    return subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.api.app:app", "--port", "8001"],
        cwd=ROOT_DIR
    )

def run_frontend():
    print("[SKYNET] Starting Frontend...")
    return subprocess.Popen(
        "cd frontend && npm run dev",
        cwd=ROOT_DIR,
        shell=True
    )

def main():
    print("[SKYNET] Initializing Startup Manager...")
    
    mcp_process = run_mcp()
    time.sleep(2)
    
    backend_process = run_backend()
    time.sleep(2)
    
    frontend_process = run_frontend()
    
    try:
        while True:
            # Auto-restart checks
            if mcp_process.poll() is not None:
                print("[SKYNET] MCP Server crashed. Restarting...")
                mcp_process = run_mcp()
            
            if backend_process.poll() is not None:
                print("[SKYNET] FastAPI Backend crashed. Restarting...")
                backend_process = run_backend()
                
            if frontend_process.poll() is not None:
                print("[SKYNET] Frontend crashed. Restarting...")
                frontend_process = run_frontend()
                
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n[SKYNET] Shutting down all systems...")
        mcp_process.terminate()
        backend_process.terminate()
        frontend_process.terminate()

if __name__ == "__main__":
    main()
