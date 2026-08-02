"""Cost tracker — tính cost per scan, đảm bảo ≤ $0.30/scan."""
from dataclasses import dataclass, field

# Approximate pricing per 1M tokens (USD), cập nhật theo pricing 2026
PRICING = {
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4o": {"input": 2.5, "output": 10.0},
    "claude-haiku": {"input": 0.25, "output": 1.25},
    "claude-sonnet": {"input": 3.0, "output": 15.0},
    "gemini-1.5-flash": {"input": 0.075, "output": 0.30},
    "gemini-1.5-pro": {"input": 1.25, "output": 5.0},
    "tavily": {"per_search": 0.005},  # ~$5/1000 searches
}


@dataclass
class ScanCost:
    """Tích lũy cost trong 1 scan."""
    total_tokens_input: int = 0
    total_tokens_output: int = 0
    tavily_searches: int = 0
    cost_usd: float = 0.0
    breakdown: dict = field(default_factory=dict)

    def add_llm_call(self, model: str, tokens_in: int, tokens_out: int) -> None:
        if model not in PRICING:
            return
        p = PRICING[model]
        cost = (
            tokens_in / 1_000_000 * p["input"]
            + tokens_out / 1_000_000 * p["output"]
        )
        self.total_tokens_input += tokens_in
        self.total_tokens_output += tokens_out
        self.cost_usd += cost
        self.breakdown[model] = self.breakdown.get(model, 0.0) + cost

    def add_tavily_search(self) -> None:
        self.tavily_searches += 1
        self.cost_usd += PRICING["tavily"]["per_search"]
        self.breakdown["tavily"] = self.breakdown.get("tavily", 0.0) + PRICING["tavily"]["per_search"]

    def summary(self) -> dict:
        return {
            "total_tokens_in": self.total_tokens_input,
            "total_tokens_out": self.total_tokens_output,
            "tavily_searches": self.tavily_searches,
            "cost_usd": round(self.cost_usd, 4),
            "breakdown": self.breakdown,
        }
