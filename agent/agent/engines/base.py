"""Base engine abstract + common types."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Protocol


@dataclass
class EngineResponse:
    """Standard response từ tất cả engines (LLM hoặc Search)."""
    text: str
    citations: list[dict] = field(default_factory=list)
    model_version: str = ""
    latency_ms: int = 0
    cost_usd: float = 0.0
    raw: dict = field(default_factory=dict)
    llm_engine: str | None = None  # None nếu là search engine; 'chatgpt'|'gemini'|'claude' nếu là LLM
    search_engine: str | None = None  # None nếu là LLM; 'tavily' nếu là search

    def engine_kind(self) -> str:
        """Trả về 'llm' hoặc 'search'."""
        return "llm" if self.llm_engine else "search"


class BaseEngine(ABC):
    """Base class cho cả LLM engine và Search engine."""

    @abstractmethod
    async def query(self, prompt: str, **kwargs) -> EngineResponse:
        raise NotImplementedError

    def _estimate_cost(self, tokens_in: int, tokens_out: int, model: str) -> float:
        """Rough cost estimate cho LLM token-based. Search engine override riêng."""
        pricing = {
            "gpt-4o-mini": (0.15, 0.60),
            "gpt-4o": (2.5, 10.0),
            "claude-3-5-haiku": (0.25, 1.25),
            "claude-3-5-sonnet": (3.0, 15.0),
            "gemini-1.5-flash": (0.075, 0.30),
            "gemini-1.5-pro": (1.25, 5.0),
        }
        if model not in pricing:
            return 0.0
        inp, out = pricing[model]
        return tokens_in / 1_000_000 * inp + tokens_out / 1_000_000 * out
