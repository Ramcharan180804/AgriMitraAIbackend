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


class DiseaseDetection(Base):
    __tablename__ = "disease_detections"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    farm_id: Mapped[int] = mapped_column(
        ForeignKey("farms.id"), nullable=False, index=True
    )

    crop_id: Mapped[int | None] = mapped_column(
        ForeignKey("crops.id"), nullable=True, index=True
    )

    image_path: Mapped[str | None] = mapped_column(
        String(500), nullable=True
    )

    disease_name: Mapped[str] = mapped_column(
        String(150), nullable=False
    )

    confidence_score: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )

    symptoms: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    recommended_treatment: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    farm = relationship("Farm")
    crop = relationship("Crop")
