"""Brand endpoints — list 2 brand demo + đối thủ."""
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Brand
from app.db.session import get_session

router = APIRouter()


@router.get("/")
async def list_brands(session: AsyncSession = Depends(get_session)) -> list[dict]:
    """List all brands (2 target + 4-6 competitors)."""
    result = await session.execute(select(Brand).order_by(Brand.is_target.desc(), Brand.name))
    brands = result.scalars().all()
    return [
        {
            "id": b.id,
            "name": b.name,
            "name_variants": b.name_variants,
            "brand_type": b.brand_type,
            "is_target": b.is_target,
            "category": b.category,
            "shopee_url": b.shopee_url,
            "lazada_url": b.lazada_url,
            "website_url": b.website_url,
        }
        for b in brands
    ]
