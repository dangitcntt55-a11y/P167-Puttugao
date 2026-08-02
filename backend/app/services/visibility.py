"""Service: Visibility & SOV computation.

Tính:
- Visibility Rate: % prompt mà brand được nhắc đến
- SOV (Share of Voice): % mention của brand so với tổng mention của tất cả brand
"""
from collections import defaultdict
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Mention, Response, Brand


async def compute_visibility_rate(
    session: AsyncSession, brand_id: int, days: int = 7
) -> float:
    """Visibility Rate = (# prompt có mention brand) / (total prompts)."""
    from datetime import datetime, timedelta
    cutoff = datetime.utcnow() - timedelta(days=days)

    # Count responses trong period
    total_resp = await session.scalar(
        select(func.count(Response.id))
        .where(Response.brand_id == brand_id, Response.created_at >= cutoff)
    )
    if not total_resp:
        return 0.0

    # Count responses có mention target brand
    mentioned_resp = await session.scalar(
        select(func.count(func.distinct(Mention.response_id)))
        .join(Response, Mention.response_id == Response.id)
        .where(Response.brand_id == brand_id, Mention.is_target_brand == True, Response.created_at >= cutoff)  # noqa: E712
    )
    return mentioned_resp / total_resp if total_resp else 0.0


async def compute_sov(
    session: AsyncSession, brand_id: int, days: int = 7
) -> float:
    """SOV = mention của brand / tổng mention trong ngành hàng."""
    from datetime import datetime, timedelta
    cutoff = datetime.utcnow() - timedelta(days=days)

    # Get brand's category
    brand = await session.get(Brand, brand_id)
    if not brand:
        return 0.0

    # Total mentions of target brand
    target_mentions = await session.scalar(
        select(func.count(Mention.id))
        .join(Response, Mention.response_id == Response.id)
        .where(Response.brand_id == brand_id, Mention.is_target_brand == True, Response.created_at >= cutoff)  # noqa: E712
    )

    # Total mentions in same category
    total_mentions = await session.scalar(
        select(func.count(Mention.id))
        .join(Response, Mention.response_id == Response.id)
        .join(Brand, Response.brand_id == Brand.id)
        .where(Brand.category == brand.category, Response.created_at >= cutoff)
    )
    return target_mentions / total_mentions if total_mentions else 0.0
