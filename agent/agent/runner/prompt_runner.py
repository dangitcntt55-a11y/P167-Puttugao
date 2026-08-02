"""Prompt runner — gọi 1 engine cho 1 prompt.

Retry + exponential backoff theo tenacity.
"""
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential

from agent.engines.base import BaseEngine, EngineResponse


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
async def run_with_retry(engine: BaseEngine, prompt: str, **kwargs) -> EngineResponse:
    """Gọi engine với retry logic (3 lần, backoff 1s/2s/4s)."""
    return await engine.query(prompt, **kwargs)


async def run_one(engine: BaseEngine, prompt: str, **kwargs) -> EngineResponse:
    """Run 1 prompt × 1 engine, có retry."""
    return await run_with_retry(engine, prompt, **kwargs)
