"""Prompt ORM model — mỗi prompt trong prompt library E-commerce."""
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.base import Base


class Prompt(Base):
    __tablename__ = "prompts"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(1000), nullable=False)
    group: Mapped[str] = mapped_column(String(50), index=True)  # 'uy_tín' | 'giá' | 'so_sánh' | 'review' | 'ship'
    language: Mapped[str] = mapped_column(String(10), default="vi")
    tags: Mapped[list[str]] = mapped_column(JSON, default=list)
    difficulty: Mapped[str] = mapped_column(String(20), default="medium")  # 'easy' | 'medium' | 'hard'
    expected_mentions: Mapped[list[str]] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
