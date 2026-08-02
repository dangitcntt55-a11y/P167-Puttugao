"""Visibility endpoints — trả về Visibility Rate, SOV, Stability Score per brand.

Theo ADR-0003: query filter hỗ trợ tham số ``engine`` chung (không phân biệt
LLM vs search). Service sẽ route value tới ``llm_engine`` hoặc
``search_engine`` column tương ứng.
"""
from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.services import visibility as visibility_svc

router = APIRouter()

LLM_ENGINES = {"chatgpt", "gemini", "claude"}
SEARCH_ENGINES = {"tavily"}


@router.get("/{brand_id}")
async def get_brand_visibility(
    brand_id: int,
    days: int = Query(7, ge=1, le=90),
    engine: str | None = Query(
        None,
        description=(
            "Lọc theo engine cụ thể (chatgpt/gemini/claude/tavily). "
            "None = tất cả engines (ADR-0003 tách llm vs search)."
        ),
    ),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Trả về Visibility Rate, SOV, Stability Score trung bình cho 1 brand.

    Args:
        brand_id: ID của brand
        days: Số ngày lookback (default 7)
        engine: optional — lọc theo 1 engine cụ thể (chatgpt|gemini|claude|tavily).
            None = aggregate all engines.

    Returns:
        Dict với:
        - visibility_rate: float 0-1
        - sov: float 0-1 (share of voice)
        - avg_stability: float 0-1
        - n_responses: int
        - trend: list[dict] per day
        - engines_breakdown: dict per engine kind (llm vs search) — bonus info
    """
    # TODO: implement bằng query join responses + mentions + stability_scores
    # TODO: nếu engine ∈ LLM_ENGINES, filter Response.llm_engine == engine.
    # TODO: nếu engine ∈ SEARCH_ENGINES, filter Response.search_engine == engine.
    return {
        "brand_id": brand_id,
        "period_days": days,
        "engine_filter": engine,
        "visibility_rate": 0.0,
        "sov": 0.0,
        "avg_stability": 0.0,
        "n_responses": 0,
        "trend": [],
        "computed_at": datetime.utcnow().isoformat(),
    }