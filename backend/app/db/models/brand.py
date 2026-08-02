"""Brand ORM model — đại diện cho 1 shop/brand E-commerce (target hoặc đối thủ)."""
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Brand(Base):
    __tablename__ = "brands"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name_variants: Mapped[list[str]] = mapped_column(JSON, default=list)  # ['Minh Long', 'Minh Long Book', 'MLB']
    brand_type: Mapped[str] = mapped_column(String(50))  # 'sàn' | 'd2c' | 'retailer'
    is_target: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    category: Mapped[str] = mapped_column(String(100))  # ngành hàng chính
    shopee_url: Mapped[str | None] = mapped_column(String(500))
    lazada_url: Mapped[str | None] = mapped_column(String(500))
    website_url: Mapped[str | None] = mapped_column(String(500))
    knowledge_base: Mapped[dict] = mapped_column(JSON, default=dict)  # {price_table, ship_policy, faq, rating}
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    responses: Mapped[list["Response"]] = relationship(back_populates="brand")  # noqa: F821
    stability_scores: Mapped[list["StabilityScore"]] = relationship(back_populates="brand")  # noqa: F821
