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


class FarmingActivity(Base):
    __tablename__ = "farming_activities"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    farm_id: Mapped[int] = mapped_column(
        ForeignKey("farms.id"), nullable=False, index=True
    )

    activity_type: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    activity_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    description: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    resource_used: Mapped[str | None] = mapped_column(
        String(150), nullable=True
    )

    quantity_used: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )

    cost: Mapped[float] = mapped_column(
        Float, nullable=False, default=0
    )

    notes: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    farm = relationship("Farm")
