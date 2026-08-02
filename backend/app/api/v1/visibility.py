"""Visibility endpoints — trả về Visibility Rate, SOV, Stability Score per brand."""
from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.services import visibility as visibility_svc

router = APIRouter()


@router.get("/{brand_id}")
async def get_brand_visibility(
    brand_id: int,
    days: int = Query(7, ge=1, le=90),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Trả về Visibility Rate, SOV, Stability Score trung bình cho 1 brand.

    Args:
        brand_id: ID của brand
        days: Số ngày lookback (default 7)

    Returns:
        Dict với:
        - visibility_rate: float 0-1
        - sov: float 0-1 (share of voice)
        - avg_stability: float 0-1
        - n_responses: int
        - trend: list[dict] per day
    """
    # TODO: implement bằng query join responses + mentions + stability_scores
    return {
        "brand_id": brand_id,
        "period_days": days,
        "visibility_rate": 0.0,
        "sov": 0.0,
        "avg_stability": 0.0,
        "n_responses": 0,
        "trend": [],
        "computed_at": datetime.utcnow().isoformat(),
    }
