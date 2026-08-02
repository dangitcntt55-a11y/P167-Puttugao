"""Response ORM model — raw response từ 4 nguồn AI (ChatGPT, Gemini, Claude, Tavily)."""
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Response(Base):
    __tablename__ = "responses"

    id: Mapped[int] = mapped_column(primary_key=True)
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"), index=True)
    prompt_id: Mapped[int] = mapped_column(ForeignKey("prompts.id"), index=True)
    ai_engine: Mapped[str] = mapped_column(String(20), index=True)  # 'chatgpt' | 'gemini' | 'claude' | 'tavily'
    model_version: Mapped[str] = mapped_column(String(100))
    response_text: Mapped[str] = mapped_column(Text, nullable=False)
    citations: Mapped[dict] = mapped_column(JSON, default=dict)  # URL citation mà AI/Tavily tham chiếu
    run_index: Mapped[int] = mapped_column(Integer, index=True)  # 1, 2, 3 (3 lần/prompt/ngày)
    latency_ms: Mapped[int | None] = mapped_column(Integer)
    cost_usd: Mapped[float | None] = mapped_column()
    trace_id: Mapped[str | None] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), index=True)

    # Relationships
    brand: Mapped["Brand"] = relationship(back_populates="responses")  # noqa: F821
    mentions: Mapped[list["Mention"]] = relationship(back_populates="response", cascade="all, delete-orphan")  # noqa: F821
