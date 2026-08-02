"""Tavily engine — web-grounded search với citation built-in.

Tavily dùng cho:
1. Cross-check claim giá/ship/uy tín với web public
2. Verify hallucination AI
3. KHÔNG dùng để parse mention (dùng ChatGPT/Claude parser)
"""
import time
from tavily import AsyncTavilyClient

from agent.config import settings
from agent.engines.base import BaseEngine, EngineResponse


class TavilyEngine(BaseEngine):
    search_engine = "tavily"

    def __init__(self):
        self.client = AsyncTavilyClient(api_key=settings.tavily_api_key)

    async def query(self, prompt: str, **kwargs) -> EngineResponse:
        """Tavily search với prompt dạng natural language question."""
        start = time.perf_counter()
        response = await self.client.search(
            query=prompt,
            search_depth=kwargs.get("search_depth", "advanced"),  # 'basic' | 'advanced'
            max_results=kwargs.get("max_results", 5),
            include_answer=kwargs.get("include_answer", True),
            include_raw_content=kwargs.get("include_raw_content", False),
            topic=kwargs.get("topic", "general"),
        )
        latency_ms = int((time.perf_counter() - start) * 1000)

        # Tavily trả về answer + citations
        answer = response.get("answer", "")
        results = response.get("results", [])
        citations = [
            {"url": r.get("url"), "title": r.get("title"), "content": r.get("content")}
            for r in results
        ]

        # Cost ước lượng: ~$0.005/search
        cost = 0.005

        return EngineResponse(
            text=answer,
            citations=citations,
            model_version="tavily-advanced",
            latency_ms=latency_ms,
            cost_usd=cost,
            raw=response,
            search_engine=self.search_engine,
        )
