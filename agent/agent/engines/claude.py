"""Claude engine — claude-3-5-haiku (cheap) / claude-3-5-sonnet (heavy)."""
import time
import anthropic

from agent.config import settings
from agent.engines.base import BaseEngine, EngineResponse


class ClaudeEngine(BaseEngine):
    llm_engine = "claude"

    def __init__(self, model: str = "claude-3-5-haiku-20241022"):
        self.model = model
        self.client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

    async def query(self, prompt: str, **kwargs) -> EngineResponse:
        start = time.perf_counter()
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=kwargs.get("max_tokens", 1024),
            messages=[{"role": "user", "content": prompt}],
        )
        latency_ms = int((time.perf_counter() - start) * 1000)

        text = ""
        for block in response.content:
            if hasattr(block, "text"):
                text += block.text

        cost = self._estimate_cost(response.usage.input_tokens, response.usage.output_tokens, self.model)

        return EngineResponse(
            text=text,
            citations=[],
            model_version=self.model,
            latency_ms=latency_ms,
            cost_usd=cost,
            raw=response.model_dump(),
            llm_engine=self.llm_engine,
        )
