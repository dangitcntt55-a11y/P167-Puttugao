"""StabilityScore ORM model — Stability Score per (brand, prompt).

Theo ADR-0003: cột engine cũng tách thành `llm_engine` + `search_engine` (chỉ 1 trong 2 NOT NULL).
Cho phép cả 2 NULL = aggregate overall score (cross-engine).
"""
from datetime import datetime
from sqlalchemy import String, Integer, Float, ForeignKey, DateTime, Boolean, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base


class StabilityScore(Base):
    __tablename__ = "stability_scores"

    id: Mapped[int] = mapped_column(primary_key=True)
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"), index=True)
    prompt_id: Mapped[int] = mapped_column(ForeignKey("prompts.id"), index=True)
    llm_engine: Mapped[str | None] = mapped_column(String(20), nullable=True)  # NULL | 'chatgpt' | 'gemini' | 'claude'
    search_engine: Mapped[str | None] = mapped_column(String(20), nullable=True)  # NULL | 'tavily'
    stability_score: Mapped[float] = mapped_column(Float)  # 1 - normalized variance
    visibility_rate: Mapped[float] = mapped_column(Float)  # 0-1
    n_runs: Mapped[int] = mapped_column(Integer)
    is_stable: Mapped[bool] = mapped_column(Boolean, index=True)  # TRUE if score >= 0.7
    computed_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), index=True)

    __table_args__ = (
        CheckConstraint(
            "(llm_engine IS NOT NULL AND search_engine IS NULL) "
            "OR (llm_engine IS NULL AND search_engine IS NOT NULL) "
            "OR (llm_engine IS NULL AND search_engine IS NULL)",
            name="chk_stability_one_engine",
        ),
    )

    # Relationships
    brand: Mapped["Brand"] = relationship(back_populates="stability_scores")  # noqa: F821