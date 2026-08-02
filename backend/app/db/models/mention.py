"""Mention ORM model — extracted mention từ response."""
from datetime import datetime
from sqlalchemy import String, Integer, Float, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Mention(Base):
    __tablename__ = "mentions"

    id: Mapped[int] = mapped_column(primary_key=True)
    response_id: Mapped[int] = mapped_column(ForeignKey("responses.id", ondelete="CASCADE"), index=True)
    brand_name: Mapped[str] = mapped_column(String(255), index=True)
    is_target_brand: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    position: Mapped[int] = mapped_column(Integer)  # 1, 2, 3 (vị trí nhắc đến)
    sentiment: Mapped[float] = mapped_column(Float)  # -1 to +1
    context_quote: Mapped[str] = mapped_column(Text)
    claim_type: Mapped[str] = mapped_column(String(20))  # 'price' | 'ship' | 'review' | 'general'
    confidence: Mapped[float] = mapped_column(Float, default=1.0)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)  # HITL verified
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relationships
    response: Mapped["Response"] = relationship(back_populates="mentions")  # noqa: F821
