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


class Evaluation(Base):
    __tablename__ = "evaluations"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    farm_id: Mapped[int] = mapped_column(
        ForeignKey("farms.id"),
        nullable=False,
        index=True,
    )

    crop_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    yield_quantity: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    quality_rating: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    total_cost: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0,
    )

    profit: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    evaluated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    farm = relationship("Farm")
