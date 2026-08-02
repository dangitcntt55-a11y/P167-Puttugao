"""Celery tasks for periodic scans.

Theo ADR-0003: tham số ``engines`` (rename từ ``ai_engines``) chấp nhận cả
LLM (chatgpt/claude/gemini) và search engine (tavily).
"""
from app.workers.celery_app import celery_app


@celery_app.task(name="scan.run_full_scan")
def run_full_scan(brand_id: int, prompt_ids: list[int] | None = None, engines: list[str] | None = None, n_runs: int = 3) -> dict:
    """Trigger full scan cho 1 brand.

    Args:
        brand_id: ID của brand
        prompt_ids: list prompt IDs (None = all)
        engines: list engine names (None = all 4: chatgpt/claude/gemini/tavily).
            Agent orchestrator sẽ route value tới ``llm_engine`` hoặc
            ``search_engine`` column khi lưu ``responses`` row.
        n_runs: số lần chạy/prompt (default 3)

    Returns:
        Dict summary: {n_responses, n_engines, cost_usd, ...}
    """
    # TODO: gọi agent runner thật
    return {
        "status": "completed",
        "brand_id": brand_id,
        "n_responses": 0,
        "message": "TODO: integrate with agent/",
    }