"""ChatGPT engine — gpt-4o-mini (cheap) / gpt-4o (heavy)."""
import time
import openai

from agent.config import settings
from agent.engines.base import BaseEngine, EngineResponse


class ChatGPTEngine(BaseEngine):
    llm_engine = "chatgpt"

    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self.client = openai.AsyncOpenAI(api_key=settings.openai_api_key)

    async def query(self, prompt: str, **kwargs) -> EngineResponse:
        start = time.perf_counter()
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 1024),
        )
        latency_ms = int((time.perf_counter() - start) * 1000)

        text = response.choices[0].message.content or ""
        usage = response.usage
        cost = self._estimate_cost(usage.prompt_tokens, usage.completion_tokens, self.model)

        return EngineResponse(
            text=text,
            citations=[],
            model_version=self.model,
            latency_ms=latency_ms,
            cost_usd=cost,
            raw=response.model_dump(),
            llm_engine=self.llm_engine,
        )
