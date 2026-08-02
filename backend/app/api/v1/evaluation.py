"""Evaluation endpoints — closed-loop re-measurement report."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Task
from app.db.session import get_session

router = APIRouter()


@router.get("/{task_id}")
async def get_evaluation_report(task_id: int, session: AsyncSession = Depends(get_session)) -> dict:
    """Closed-loop evaluation report cho 1 task.

    Returns:
        Dict với:
        - task_id
        - pre_visibility: float 0-1
        - post_visibility: float 0-1
        - difference: float (post - pre)
        - ci_lower, ci_upper: bootstrap 95% CI
        - result: 'improved' | 'no_evidence' | 'regressed'
        - noise_floor: float (5-7%)
        - verdict_explanation: str
    """
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {
        "task_id": task_id,
        "brand_id": task.brand_id,
        "action_type": task.action_type,
        "pre_visibility": task.pre_visibility,
        "post_visibility": task.post_visibility,
        "ci_lower": task.ci_lower,
        "ci_upper": task.ci_upper,
        "result": task.result,
        "completed_at": task.completed_at.isoformat() if task.completed_at else None,
    }
