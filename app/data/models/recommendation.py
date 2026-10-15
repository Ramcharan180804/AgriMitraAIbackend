from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.data.database.models import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    farm_id: Mapped[int] = mapped_column(
        ForeignKey("farms.id"), nullable=False, index=True
    )

    crop_id: Mapped[int] = mapped_column(
        ForeignKey("crops.id"), nullable=False, index=True
    )

    confidence_score: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )

    recommendation_reason: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    season: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    farm = relationship("Farm")
    crop = relationship("Crop")
