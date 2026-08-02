"""Celery tasks for periodic scans."""
from app.workers.celery_app import celery_app


@celery_app.task(name="scan.run_full_scan")
def run_full_scan(brand_id: int, prompt_ids: list[int] | None = None, ai_engines: list[str] | None = None, n_runs: int = 3) -> dict:
    """Trigger full scan cho 1 brand.

    Args:
        brand_id: ID của brand
        prompt_ids: list prompt IDs (None = all)
        ai_engines: list ['chatgpt', 'gemini', 'claude', 'tavily'] (None = all)
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
