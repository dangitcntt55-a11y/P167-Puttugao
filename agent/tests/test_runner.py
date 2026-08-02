"""Test prompt runner với mock."""
import pytest
from agent.runner.prompt_runner import run_one
from agent.engines.base import BaseEngine, EngineResponse


class MockEngine(BaseEngine):
    llm_engine = "mock"  # giả LLM để test

    def __init__(self, response_text: str = "Mock response"):
        self.response_text = response_text

    async def query(self, prompt: str, **kwargs) -> EngineResponse:
        return EngineResponse(
            text=self.response_text,
            citations=[],
            model_version="mock-1.0",
            latency_ms=10,
            cost_usd=0.0,
            llm_engine="mock",
        )


@pytest.mark.asyncio
async def test_run_one():
    engine = MockEngine("Test response")
    response = await run_one(engine, "Test prompt")
    assert response.text == "Test response"
    assert response.llm_engine == "mock"
    assert response.search_engine is None
    assert response.engine_kind() == "llm"
