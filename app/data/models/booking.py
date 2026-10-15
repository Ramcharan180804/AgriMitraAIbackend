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


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    farmer_id: Mapped[int] = mapped_column(
        ForeignKey("farmers.id"), nullable=False, index=True
    )

    resource_id: Mapped[int] = mapped_column(
        ForeignKey("resources.id"), nullable=False, index=True
    )

    quantity: Mapped[float] = mapped_column(
        Float, nullable=False
    )

    total_price: Mapped[float] = mapped_column(
        Float, nullable=False
    )

    booking_status: Mapped[str] = mapped_column(
        String(30), nullable=False, default="PENDING"
    )

    booking_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    notes: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    farmer = relationship("Farmer")
    resource = relationship("Resource")
