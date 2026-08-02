"""Scan endpoints — trigger manual scan (sẽ gọi agent/)."""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session

router = APIRouter()


class ScanRequest(BaseModel):
    brand_id: int
    prompt_ids: list[int] | None = None  # None = all prompts
    ai_engines: list[str] | None = None  # None = all 4 engines
    n_runs: int = 3


class ScanResponse(BaseModel):
    task_id: str
    status: str
    brand_id: int
    n_prompts: int
    n_engines: int


@router.post("/")
async def trigger_scan(req: ScanRequest, session: AsyncSession = Depends(get_session)) -> ScanResponse:
    """Trigger 1 scan (manual). Sẽ queue Celery task.

    LUỒNG:
    1. Validate brand_id + prompt_ids
    2. Dispatch Celery task `run_scan`
    3. Return task_id cho client poll
    """
    # TODO: dispatch Celery task thật
    # from app.workers.scan_tasks import run_scan
    # task = run_scan.delay(req.brand_id, req.prompt_ids, req.ai_engines, req.n_runs)
    return ScanResponse(
        task_id="pending-impl",
        status="queued",
        brand_id=req.brand_id,
        n_prompts=len(req.prompt_ids) if req.prompt_ids else 100,
        n_engines=len(req.ai_engines) if req.ai_engines else 4,
    )
