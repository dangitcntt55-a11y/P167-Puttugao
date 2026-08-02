"""Diagnosis ORM model — output từ Diagnosis Agent."""
from datetime import datetime
from sqlalchemy import String, Integer, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.base import Base


class Diagnosis(Base):
    __tablename__ = "diagnoses"

    id: Mapped[int] = mapped_column(primary_key=True)
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"), index=True)
    prompt_id: Mapped[int] = mapped_column(ForeignKey("prompts.id"), index=True)
    is_stable: Mapped[bool] = mapped_column()
    stability_score: Mapped[float] = mapped_column(Float)
    hypotheses: Mapped[list[dict]] = mapped_column(JSON, default=list)
    # [{hypothesis, confidence, evidence_urls: [url], quote_span: str, claim_type: str}]
    evidence_package: Mapped[dict] = mapped_column(JSON, default=dict)
    recommended_actions: Mapped[list[dict]] = mapped_column(JSON, default=list)
    severity: Mapped[str] = mapped_column(String(20), default="medium")  # 'low' | 'medium' | 'high' | 'critical'
    status: Mapped[str] = mapped_column(String(20), default="pending_review", index=True)
    # 'pending_review' | 'approved' | 'rejected' | 'in_progress'
    reviewed_by: Mapped[str | None] = mapped_column(String(100))
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), index=True)
