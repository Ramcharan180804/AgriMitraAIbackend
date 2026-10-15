from sqlalchemy import Boolean, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.data.database.models import Base


class Crop(Base):
    __tablename__ = "crops"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    crop_name: Mapped[str] = mapped_column(
        String(100), nullable=False, index=True
    )

    scientific_name: Mapped[str | None] = mapped_column(
        String(150), nullable=True
    )

    crop_type: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )

    suitable_soil: Mapped[str | None] = mapped_column(
        String(150), nullable=True
    )

    min_temperature: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )

    max_temperature: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )

    min_rainfall: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )

    max_rainfall: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )

    description: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )
