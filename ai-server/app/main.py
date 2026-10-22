"""DocuForge AI Server (FastAPI + Ollama gemma4:12b)."""
from fastapi import FastAPI

from app.config import get_settings
from app.models.schemas import HealthResponse
from app.routers import ask, summarize
from app.services import ollama_client

app = FastAPI(title="DocuForge AI Server", version="1.0.0")
app.include_router(summarize.router, tags=["summarize"])
app.include_router(ask.router, tags=["ask"])


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        status="ok",
        model=settings.ollama_model,
        embed_model=settings.ollama_embed_model or None,
        ollama=await ollama_client.ping(),
    )
