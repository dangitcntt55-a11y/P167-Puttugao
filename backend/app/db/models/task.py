"""Task ORM model — task theo dõi hành động tối ưu + closed-loop."""
from datetime import datetime
from sqlalchemy import String, Integer, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.base import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"), index=True)
    diagnosis_id: Mapped[int | None] = mapped_column(ForeignKey("diagnoses.id"), index=True)
    action_type: Mapped[str] = mapped_column(String(50))
    # 'listing_update' | 'schema_add' | 'outreach' | 'content_pr' | 'content_add'
    action_payload: Mapped[dict] = mapped_column(JSON, default=dict)
    owner_team: Mapped[str | None] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(20), default="todo", index=True)
    # 'todo' | 'in_progress' | 'done' | 'cancelled'
    pre_scan_id: Mapped[int | None] = mapped_column(ForeignKey("responses.id"))
    post_scan_id: Mapped[int | None] = mapped_column(ForeignKey("responses.id"))
    result: Mapped[str | None] = mapped_column(String(20), index=True)
    # 'improved' | 'no_evidence' | 'regressed'
    ci_lower: Mapped[float | None] = mapped_column(Float)
    ci_upper: Mapped[float | None] = mapped_column(Float)
    pre_visibility: Mapped[float | None] = mapped_column(Float)
    post_visibility: Mapped[float | None] = mapped_column(Float)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), index=True)
