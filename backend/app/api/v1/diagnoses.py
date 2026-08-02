"""Diagnosis endpoints — list qua Stability filter + HITL approve/reject."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Diagnosis
from app.db.session import get_session
from app.config import settings

router = APIRouter()


@router.get("/")
async def list_diagnoses(
    brand_id: int | None = Query(None),
    stable_only: bool = Query(True, description="Chỉ lấy diagnoses có Stability >= 0.7"),
    status: str | None = Query(None),
    session: AsyncSession = Depends(get_session),
) -> list[dict]:
    """List diagnoses, mặc định chỉ lấy stable (Stability >= 0.7)."""
    query = select(Diagnosis)
    if brand_id:
        query = query.where(Diagnosis.brand_id == brand_id)
    if stable_only:
        query = query.where(Diagnosis.is_stable == True, Diagnosis.stability_score >= settings.stability_threshold)  # noqa: E712
    if status:
        query = query.where(Diagnosis.status == status)
    query = query.order_by(Diagnosis.severity.desc(), Diagnosis.created_at.desc())

    result = await session.execute(query)
    diagnoses = result.scalars().all()
    return [
        {
            "id": d.id,
            "brand_id": d.brand_id,
            "prompt_id": d.prompt_id,
            "is_stable": d.is_stable,
            "stability_score": d.stability_score,
            "hypotheses": d.hypotheses,
            "evidence_package": d.evidence_package,
            "recommended_actions": d.recommended_actions,
            "severity": d.severity,
            "status": d.status,
            "created_at": d.created_at.isoformat() if d.created_at else None,
        }
        for d in diagnoses
    ]


@router.post("/{diagnosis_id}/approve")
async def approve_diagnosis(diagnosis_id: int, session: AsyncSession = Depends(get_session)) -> dict:
    """HITL approve diagnosis → tạo task."""
    diagnosis = await session.get(Diagnosis, diagnosis_id)
    if not diagnosis:
        raise HTTPException(status_code=404, detail="Diagnosis not found")
    diagnosis.status = "approved"
    diagnosis.reviewed_at = __import__("datetime").datetime.utcnow()
    await session.commit()
    # TODO: tạo task từ recommended_actions
    return {"diagnosis_id": diagnosis_id, "status": "approved"}


@router.post("/{diagnosis_id}/reject")
async def reject_diagnosis(diagnosis_id: int, session: AsyncSession = Depends(get_session)) -> dict:
    """HITL reject diagnosis."""
    diagnosis = await session.get(Diagnosis, diagnosis_id)
    if not diagnosis:
        raise HTTPException(status_code=404, detail="Diagnosis not found")
    diagnosis.status = "rejected"
    diagnosis.reviewed_at = __import__("datetime").datetime.utcnow()
    await session.commit()
    return {"diagnosis_id": diagnosis_id, "status": "rejected"}
