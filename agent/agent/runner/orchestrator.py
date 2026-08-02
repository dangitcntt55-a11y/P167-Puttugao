"""Orchestrator — scan N lần × 4 AI cho 1 brand.

Schedule:
    for each prompt in prompt_ids:
        for each ai_engine in ai_engines:
            for run_index in range(n_runs):
                response = engine.query(prompt)
                save_to_backend(response)
"""
import asyncio
import httpx
from typing import Iterable

from agent.config import settings
from agent.engines.chatgpt import ChatGPTEngine
from agent.engines.claude import ClaudeEngine
from agent.engines.gemini import GeminiEngine
from agent.engines.tavily import TavilyEngine
from agent.engines.base import BaseEngine, EngineResponse
from agent.runner.prompt_runner import run_one


def get_engine(engine_name: str) -> BaseEngine:
    """Map engine name → engine instance."""
    mapping = {
        "chatgpt": lambda: ChatGPTEngine(model="gpt-4o-mini"),
        "claude":  lambda: ClaudeEngine(model="claude-3-5-haiku-20241022"),
        "gemini":  lambda: GeminiEngine(model="gemini-1.5-flash"),
        "tavily":  lambda: TavilyEngine(),
    }
    if engine_name not in mapping:
        raise ValueError(f"Unknown engine: {engine_name}. Valid: {list(mapping)}")
    return mapping[engine_name]()


def get_all_engines() -> list[BaseEngine]:
    """Default 4 engines cho demo (3 LLM + 1 Search)."""
    return [
        get_engine("chatgpt"),
        get_engine("claude"),
        get_engine("gemini"),
        get_engine("tavily"),
    ]


async def save_response_to_backend(brand_id: int, prompt_id: int, response: EngineResponse, run_index: int) -> dict:
    """POST response về backend API để lưu DB."""
    async with httpx.AsyncClient() as client:
        payload = {
            "brand_id": brand_id,
            "prompt_id": prompt_id,
            "model_version": response.model_version,
            "response_text": response.text,
            "citations": response.citations,
            "run_index": run_index,
            "latency_ms": response.latency_ms,
            "cost_usd": response.cost_usd,
        }
        if response.llm_engine:
            payload["llm_engine"] = response.llm_engine
        if response.search_engine:
            payload["search_engine"] = response.search_engine
        r = await client.post(
            f"{settings.backend_api_url}/responses/",
            json=payload,
            headers={"X-API-Key": settings.backend_api_key} if settings.backend_api_key else {},
        )
        r.raise_for_status()
        return r.json()


async def fetch_prompts(brand_id: int, prompt_ids: list[int] | None = None) -> list[dict]:
    """Lấy prompt list từ backend."""
    async with httpx.AsyncClient() as client:
        params = {"brand_id": brand_id}
        if prompt_ids:
            params["ids"] = ",".join(map(str, prompt_ids))
        r = await client.get(f"{settings.backend_api_url}/prompts/", params=params)
        r.raise_for_status()
        return r.json()


async def run_scan(
    brand_id: int,
    prompt_ids: list[int] | None = None,
    ai_engines: list[str] | None = None,
    n_runs: int = 3,
) -> dict:
    """Scan main entry.

    Args:
        brand_id: ID brand
        prompt_ids: list prompt IDs (None = all)
        ai_engines: list engine names (None = all 4)
        n_runs: số lần chạy/prompt (default 3)

    Returns:
        Dict summary: {n_responses, cost_usd, by_engine}
    """
    # 1. Get prompts
    prompts = await fetch_prompts(brand_id, prompt_ids)
    if not prompts:
        return {"status": "no_prompts", "n_responses": 0}

    # 2. Get engines
    engines = get_all_engines() if not ai_engines else [get_engine(e) for e in ai_engines]

    # 3. Iterate
    total_cost = 0.0
    n_responses = 0
    by_llm: dict[str, int] = {}
    by_search: dict[str, int] = {}

    for prompt in prompts:
        for engine in engines:
            for run_index in range(1, n_runs + 1):
                try:
                    response = await run_one(engine, prompt["text"])
                    await save_response_to_backend(brand_id, prompt["id"], response, run_index)
                    total_cost += response.cost_usd
                    n_responses += 1
                    if response.llm_engine:
                        by_llm[response.llm_engine] = by_llm.get(response.llm_engine, 0) + 1
                    elif response.search_engine:
                        by_search[response.search_engine] = by_search.get(response.search_engine, 0) + 1
                except Exception as e:
                    print(f"[ERROR] engine={getattr(engine, 'llm_engine', None) or getattr(engine, 'search_engine', '?')} prompt={prompt['id']} run={run_index}: {e}")

    return {
        "status": "completed",
        "brand_id": brand_id,
        "n_prompts": len(prompts),
        "n_engines": len(engines),
        "n_runs": n_runs,
        "n_responses": n_responses,
        "cost_usd": round(total_cost, 4),
        "by_llm_engine": by_llm,
        "by_search_engine": by_search,
    }
