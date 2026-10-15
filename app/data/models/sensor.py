from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.data.database.models import Base


class Sensor(Base):
    __tablename__ = "sensors"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    farm_id: Mapped[int] = mapped_column(
        ForeignKey("farms.id"), nullable=False, index=True
    )

    sensor_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )

    value: Mapped[float] = mapped_column(
        Float, nullable=False
    )

    unit: Mapped[str] = mapped_column(
        String(20), nullable=False
    )

    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    farm = relationship("Farm")
