"""FastAPI application entrypoint.

Mục đích: khởi tạo FastAPI app, kết nối DB, register routers, log startup info.
"""
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.config import settings
from app.core.logging import configure_logging
from app.db.session import engine

configure_logging(settings.log_level)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Manage startup + shutdown lifecycle."""
    # Startup
    await engine.connect()
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title="GEO AI Agent for E-commerce VN",
    version="0.1.0",
    description="Stability-aware Visibility Monitoring + Evidence-grounded Diagnosis + Closed-loop Re-measurement",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "version": app.version}
