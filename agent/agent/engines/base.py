"""Base engine abstract + common types."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Protocol


@dataclass
class EngineResponse:
    """Standard response từ tất cả 4 engines."""
    text: str
    citations: list[dict] = field(default_factory=list)
    model_version: str = ""
    latency_ms: int = 0
    cost_usd: float = 0.0
    raw: dict = field(default_factory=dict)
    ai_engine: str = ""  # 'chatgpt' | 'gemini' | 'claude' | 'tavily'


class BaseEngine(ABC):
    """Base class cho 4 engines."""

    ai_engine: str = "base"

    @abstractmethod
    async def query(self, prompt: str, **kwargs) -> EngineResponse:
        """Send prompt và nhận response."""
        raise NotImplementedError

    def _estimate_cost(self, tokens_in: int, tokens_out: int, model: str) -> float:
        """Rough cost estimate. Override nếu cần chính xác hơn."""
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
