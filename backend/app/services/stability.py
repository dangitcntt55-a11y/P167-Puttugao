"""Service: Stability Score computation.

Stability Score = 1 - normalized variance của mention_count qua N lần chạy.

Theo Schulte et al. arXiv 2604.07585:
- Cần chạy ≥ 7-8 lần/prompt/ngày để có SE < 0.10
- Demo: N=3, production: N=7-8
- Stability ≥ 0.7 mới đưa gap vào diagnosis
"""
import numpy as np
from collections import defaultdict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Response, StabilityScore
from app.config import settings


def compute_stability_score(mention_counts: list[int]) -> float:
    """Tính Stability Score = 1 - normalized variance.

    Args:
        mention_counts: list số mention qua N lần chạy (vd: [1, 1, 0, 1])

    Returns:
        Float 0-1. Càng cao càng ổn định. ≥ 0.7 mới đủ gate.

    Công thức:
        var = variance(mention_counts)
        max_var = max possible variance (Bernoulli: 0.25 cho N=3, 0.5 cho N>> )
        stability = 1 - (var / max_var)
    """
    if not mention_counts:
        return 0.0
    arr = np.array(mention_counts, dtype=float)
    var = arr.var()
    # Normalize bằng max possible variance (cho binary outcome)
    max_var = 0.25
    normalized = min(var / max_var, 1.0)
    return float(1.0 - normalized)


async def compute_stability_for_brand_prompt(
    session: AsyncSession, brand_id: int, prompt_id: int, ai_engine: str | None = None
) -> StabilityScore:
    """Tính Stability Score cho (brand, prompt, optional ai_engine) từ N lần chạy gần nhất."""
    query = (
        select(Response)
        .where(Response.brand_id == brand_id, Response.prompt_id == prompt_id)
        .order_by(Response.created_at.desc())
        .limit(settings.n_runs_per_prompt)
    )
    if ai_engine:
        query = query.where(Response.ai_engine == ai_engine)
    result = await session.execute(query)
    responses = result.scalars().all()

    # mention_count = 1 nếu có mention target brand, 0 nếu không
    # TODO: thực tế cần join bảng mentions
    mention_counts = [1 if r.mentions else 0 for r in responses]
    visibility_rate = sum(mention_counts) / len(mention_counts) if mention_counts else 0.0
    stability = compute_stability_score(mention_counts)

    score = StabilityScore(
        brand_id=brand_id,
        prompt_id=prompt_id,
        ai_engine=ai_engine or "all",
        stability_score=stability,
        visibility_rate=visibility_rate,
        n_runs=len(mention_counts),
        is_stable=stability >= settings.stability_threshold,
    )
    session.add(score)
    await session.commit()
    return score
