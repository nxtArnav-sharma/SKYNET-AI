from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import router

app = FastAPI(
    title="SKYNET CORE",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for the Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For dev only, restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def root():
    return {
        "system": "SKYNET",
        "status": "online"
    }

@app.get("/health")
def health():
    return {
        "system": "SKYNET",
        "status": "online"
    }

if __name__ == "__main__":
    import uvicorn
    from backend.config.settings import settings
    uvicorn.run("backend.api.app:app", host="0.0.0.0", port=settings.API_PORT, reload=True)
