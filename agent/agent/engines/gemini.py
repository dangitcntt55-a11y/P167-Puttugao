"""Gemini engine — gemini-1.5-flash (cheap) / gemini-1.5-pro (heavy)."""
import time
import google.generativeai as genai

from agent.config import settings
from agent.engines.base import BaseEngine, EngineResponse

# Configure API key globally
genai.configure(api_key=settings.google_ai_api_key)


class GeminiEngine(BaseEngine):
    ai_engine = "gemini"

    def __init__(self, model: str = "gemini-1.5-flash"):
        self.model = model
        self.client = genai.GenerativeModel(model)

    async def query(self, prompt: str, **kwargs) -> EngineResponse:
        start = time.perf_counter()
        # Gemini sync API; wrap in asyncio.to_thread nếu cần
        response = await _to_thread(self.client.generate_content, prompt)
        latency_ms = int((time.perf_counter() - start) * 1000)

        text = response.text if hasattr(response, "text") else ""

        # Token count
        try:
            tokens_in = response.usage_metadata.prompt_token_count
            tokens_out = response.usage_metadata.candidates_token_count
        except Exception:
            tokens_in, tokens_out = 0, 0
        cost = self._estimate_cost(tokens_in, tokens_out, self.model)

        return EngineResponse(
            text=text,
            citations=[],
            model_version=self.model,
            latency_ms=latency_ms,
            cost_usd=cost,
            raw={"text": text},
            ai_engine=self.ai_engine,
        )


async def _to_thread(func, *args, **kwargs):
    """Helper: chạy sync function trong thread pool."""
    import asyncio
    return await asyncio.to_thread(func, *args, **kwargs)
