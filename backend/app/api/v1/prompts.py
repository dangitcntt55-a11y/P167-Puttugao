"""Prompt endpoints — list prompt library (~100 prompts / 5 nhóm)."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Prompt
from app.db.session import get_session

router = APIRouter()


@router.get("/")
async def list_prompts(
    group: str | None = Query(None, description="Filter theo nhóm: uy_tín, giá, so_sánh, review, ship"),
    session: AsyncSession = Depends(get_session),
) -> list[dict]:
    """List prompts trong prompt library."""
    query = select(Prompt)
    if group:
        query = query.where(Prompt.group == group)
    result = await session.execute(query.order_by(Prompt.group, Prompt.id))
    prompts = result.scalars().all()
    return [
        {
            "id": p.id,
            "text": p.text,
            "group": p.group,
            "language": p.language,
            "tags": p.tags,
            "difficulty": p.difficulty,
        }
        for p in prompts
    ]
