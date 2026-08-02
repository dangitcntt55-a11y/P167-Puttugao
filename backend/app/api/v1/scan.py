"""Scan endpoints — trigger manual scan (sẽ gọi agent/).

Theo ADR-0003: tham số `engines` (rename từ `ai_engines`) chấp nhận cả
LLM engines (``chatgpt``/``claude``/``gemini``) và search engines (``tavily``).
Không phân biệt giữa 2 loại — agent/orchestrator sẽ route value tới đúng cột
(``llm_engine`` hoặc ``search_engine``) trong DB khi lưu response.
"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session

router = APIRouter()


class ScanRequest(BaseModel):
    brand_id: int
    prompt_ids: list[int] | None = None  # None = all prompts
    engines: list[str] | None = None  # None = all (chatgpt, claude, gemini, tavily)
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
    2. Dispatch Celery task ``run_scan``
    3. Return task_id cho client poll

    Tham số ``engines`` chấp nhận generic list engine names; agent sẽ tự
    route value vào cột ``llm_engine`` (ChatGPT/Gemini/Claude) hoặc
    ``search_engine`` (Tavily) khi lưu ``responses`` row.
    """
    # TODO: dispatch Celery task thật
    # from app.workers.scan_tasks import run_scan
    # task = run_scan.delay(req.brand_id, req.prompt_ids, req.engines, req.n_runs)
    return ScanResponse(
        task_id="pending-impl",
        status="queued",
        brand_id=req.brand_id,
        n_prompts=len(req.prompt_ids) if req.prompt_ids else 100,
        n_engines=len(req.engines) if req.engines else 4,
    )