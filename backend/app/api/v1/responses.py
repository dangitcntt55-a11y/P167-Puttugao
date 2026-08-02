"""Response endpoints — POST raw response từ agent orchestrator.

Theo ADR-0003: payload chấp nhận 1 trong 2 fields:
    - ``llm_engine`` (chatgpt | gemini | claude) → response do LLM sinh text
    - ``search_engine`` (tavily) → response là web search result

Đúng 1 trong 2 fields được set trong mỗi request (validator sẽ check).
DB có CHECK constraint ``chk_one_engine`` tương ứng.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, model_validator
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Response
from app.db.session import get_session

router = APIRouter()

LLM_ENGINES = {"chatgpt", "gemini", "claude"}
SEARCH_ENGINES = {"tavily"}


class ResponseIn(BaseModel):
    """Payload từ agent orchestrator.

    Fields:
        brand_id: FK brands
        prompt_id: FK prompts
        llm_engine: nếu là response từ LLM (chatgpt/gemini/claude)
        search_engine: nếu là response từ search engine (tavily)
        model_version: model identifier trả về (vd: gpt-4o-mini-2024-07-18)
        response_text: raw text trả về từ engine
        citations: list URL mà engine tham chiếu
        run_index: 1..N (lần chạy thứ mấy trong N lần/prompt)
        latency_ms: optional
        cost_usd: optional
        trace_id: optional trace id cho observability
    """
    brand_id: int
    prompt_id: int
    llm_engine: str | None = None
    search_engine: str | None = None
    model_version: str
    response_text: str
    citations: list[dict] | None = None
    run_index: int
    latency_ms: int | None = None
    cost_usd: float | None = None
    trace_id: str | None = None

    @model_validator(mode="after")
    def _exactly_one_engine(self) -> "ResponseIn":
        """Đảm bảo đúng 1 trong 2 engine fields được set, và value hợp lệ."""
        llm = self.llm_engine
        search = self.search_engine
        if (llm is None) == (search is None):
            raise ValueError(
                "Exactly one of llm_engine/search_engine must be set "
                "(ADR-0003 — 1 row = 1 source)."
            )
        if llm is not None and llm not in LLM_ENGINES:
            raise ValueError(
                f"llm_engine must be one of {sorted(LLM_ENGINES)}, got {llm!r}"
            )
        if search is not None and search not in SEARCH_ENGINES:
            raise ValueError(
                f"search_engine must be one of {sorted(SEARCH_ENGINES)}, got {search!r}"
            )
        return self


class ResponseOut(BaseModel):
    id: int
    brand_id: int
    prompt_id: int
    llm_engine: str | None
    search_engine: str | None
    model_version: str
    run_index: int
    created_at: str | None = None


@router.post("/", response_model=ResponseOut, status_code=201)
async def create_response(payload: ResponseIn, session: AsyncSession = Depends(get_session)) -> ResponseOut:
    """Agent gọi endpoint này để lưu 1 raw response.

    Validate theo CHECK constraint ở DB (đúng 1 trong 2 engine).
    """
    obj = Response(
        brand_id=payload.brand_id,
        prompt_id=payload.prompt_id,
        llm_engine=payload.llm_engine,
        search_engine=payload.search_engine,
        model_version=payload.model_version,
        response_text=payload.response_text,
        citations=payload.citations or [],
        run_index=payload.run_index,
        latency_ms=payload.latency_ms,
        cost_usd=payload.cost_usd,
        trace_id=payload.trace_id,
    )
    session.add(obj)
    try:
        await session.commit()
    except Exception as exc:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"DB constraint violated: {exc}")
    await session.refresh(obj)

    return ResponseOut(
        id=obj.id,
        brand_id=obj.brand_id,
        prompt_id=obj.prompt_id,
        llm_engine=obj.llm_engine,
        search_engine=obj.search_engine,
        model_version=obj.model_version,
        run_index=obj.run_index,
        created_at=obj.created_at.isoformat() if obj.created_at else None,
    )


@router.get("/{response_id}", response_model=ResponseOut)
async def get_response(response_id: int, session: AsyncSession = Depends(get_session)) -> ResponseOut:
    """Get 1 response theo ID (cho frontend xem chi tiết)."""
    obj = await session.get(Response, response_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Response not found")
    return ResponseOut(
        id=obj.id,
        brand_id=obj.brand_id,
        prompt_id=obj.prompt_id,
        llm_engine=obj.llm_engine,
        search_engine=obj.search_engine,
        model_version=obj.model_version,
        run_index=obj.run_index,
        created_at=obj.created_at.isoformat() if obj.created_at else None,
    )