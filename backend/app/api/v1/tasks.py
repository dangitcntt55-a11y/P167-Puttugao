"""Task endpoints — quản lý task + trigger re-scan closed-loop."""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Task
from app.db.session import get_session

router = APIRouter()


class TaskUpdate(BaseModel):
    status: str  # 'todo' | 'in_progress' | 'done' | 'cancelled'


@router.get("/")
async def list_tasks(
    brand_id: int | None = Query(None),
    status: str | None = Query(None),
    session: AsyncSession = Depends(get_session),
) -> list[dict]:
    """List tasks (cho frontend Kanban)."""
    query = select(Task)
    if brand_id:
        query = query.where(Task.brand_id == brand_id)
    if status:
        query = query.where(Task.status == status)
    query = query.order_by(Task.created_at.desc())
    result = await session.execute(query)
    tasks = result.scalars().all()
    return [
        {
            "id": t.id,
            "brand_id": t.brand_id,
            "diagnosis_id": t.diagnosis_id,
            "action_type": t.action_type,
            "owner_team": t.owner_team,
            "status": t.status,
            "result": t.result,
            "ci_lower": t.ci_lower,
            "ci_upper": t.ci_upper,
            "pre_visibility": t.pre_visibility,
            "post_visibility": t.post_visibility,
            "created_at": t.created_at.isoformat() if t.created_at else None,
        }
        for t in tasks
    ]


@router.patch("/{task_id}")
async def update_task(task_id: int, payload: TaskUpdate, session: AsyncSession = Depends(get_session)) -> dict:
    """Update task status. Khi status='done' → trigger re-scan qua Celery."""
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if payload.status not in {"todo", "in_progress", "done", "cancelled"}:
        raise HTTPException(status_code=400, detail="Invalid status")

    task.status = payload.status
    if payload.status == "done":
        task.completed_at = datetime.utcnow()
        # TODO: dispatch Celery task `rescan_and_eval`
        # from app.workers.rescan_tasks import rescan_and_eval
        # rescan_and_eval.delay(task_id)

    await session.commit()
    return {"task_id": task_id, "status": payload.status}
