"""Response ORM model — raw response từ LLM và Search Engine.

Theo ADR-0003: tách thành 2 cột `llm_engine` + `search_engine` (chỉ 1 trong 2 NOT NULL).
"""
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime, Text, JSON, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Response(Base):
    __tablename__ = "responses"

    id: Mapped[int] = mapped_column(primary_key=True)
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"), index=True)
    prompt_id: Mapped[int] = mapped_column(ForeignKey("prompts.id"), index=True)
    llm_engine: Mapped[str | None] = mapped_column(String(20), index=True, nullable=True)  # NULL | 'chatgpt' | 'gemini' | 'claude'
    search_engine: Mapped[str | None] = mapped_column(String(20), index=True, nullable=True)  # NULL | 'tavily'
    model_version: Mapped[str] = mapped_column(String(100))
    response_text: Mapped[str] = mapped_column(Text, nullable=False)
    citations: Mapped[dict] = mapped_column(JSON, default=dict)  # URL citation mà AI/Tavily tham chiếu
    run_index: Mapped[int] = mapped_column(Integer, index=True)  # 1, 2, 3 (3 lần/prompt/ngày)
    latency_ms: Mapped[int | None] = mapped_column(Integer)
    cost_usd: Mapped[float | None] = mapped_column()
    trace_id: Mapped[str | None] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), index=True)

    __table_args__ = (
        CheckConstraint(
            "(llm_engine IS NOT NULL AND search_engine IS NULL) OR (llm_engine IS NULL AND search_engine IS NOT NULL)",
            name="chk_one_engine",
        ),
    )

    # Relationships
    brand: Mapped["Brand"] = relationship(back_populates="responses")  # noqa: F821
    mentions: Mapped[list["Mention"]] = relationship(back_populates="response", cascade="all, delete-orphan")  # noqa: F821