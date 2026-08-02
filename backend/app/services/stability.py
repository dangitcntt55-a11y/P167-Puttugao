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


def compute_stability_score(mention_positions: list[int | None]) -> float:
    """Tính Stability Score dựa trên mention_position qua N lần chạy.

    Args:
        mention_positions: list vị trí nhắc qua N lần (None nếu không nhắc, 1/2/3 nếu có nhắc).
        Ví dụ: [1, 1, None, 2] = ổn định ở top; [None, 1, None, None] = không ổn định.

    Returns:
        Float 0-1. ≥ 0.7 mới đủ gate.

    Logic:
        - Có 2 thành phần: presence_consistency + position_consistency.
        - presence_consistency = tỷ lệ lần được nhắc (số lần != None / N).
        - position_consistency = 1 - normalized std(position) (chỉ tính trên các != None).
        - stability = 0.6 * presence_consistency + 0.4 * position_consistency.
        - Trọng số 0.6/0.4 có thể tune — giờ ưu tiên "có nhắc" hơn "đúng vị trí".
    """
    if not mention_positions:
        return 0.0
    n = len(mention_positions)
    present = [p for p in mention_positions if p is not None]
    n_present = len(present)
    presence_rate = n_present / n  # đã là 0-1

    if n_present < 2:
        # Không đủ data để tính position variance
        position_stability = presence_rate
    else:
        positions = np.array(present, dtype=float)
        if positions.std() == 0:
            position_stability = 1.0
        else:
            # Normalize std về max possible std (cho position 1-3 → max std ≈ 1.0)
            position_stability = max(0.0, 1.0 - positions.std() / 1.0)

    return float(0.6 * presence_rate + 0.4 * position_stability)


async def compute_stability_for_brand_prompt(
    session: AsyncSession, brand_id: int, prompt_id: int, llm_engine: str | None = None
) -> StabilityScore:
    """Tính Stability Score cho (brand, prompt, optional llm_engine) từ N lần chạy gần nhất."""
    query = (
        select(Response)
        .where(Response.brand_id == brand_id, Response.prompt_id == prompt_id)
        .order_by(Response.created_at.desc())
        .limit(settings.n_runs_per_prompt)
    )
    if llm_engine:
        query = query.where(Response.llm_engine == llm_engine)
    result = await session.execute(query)
    responses = result.scalars().all()

    # mention_positions = list position (None nếu brand không nhắc)
    mention_positions = []
    for r in responses:
        target_mentions = [m for m in r.mentions if m.is_target_brand]
        if target_mentions:
            # Lấy position nhỏ nhất (= nhắc sớm nhất)
            mention_positions.append(min(m.position for m in target_mentions))
        else:
            mention_positions.append(None)

    visibility_rate = sum(1 for p in mention_positions if p is not None) / len(mention_positions) if mention_positions else 0.0
    stability = compute_stability_score(mention_positions)

    score = StabilityScore(
        brand_id=brand_id,
        prompt_id=prompt_id,
        llm_engine=llm_engine,
        search_engine=None,
        stability_score=stability,
        visibility_rate=visibility_rate,
        n_runs=len(mention_positions),
        is_stable=stability >= settings.stability_threshold,
    )
    session.add(score)
    await session.commit()
    return score
