from sqlalchemy import Boolean, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.data.database.models import Base


class Resource(Base):
    __tablename__ = "resources"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    resource_name: Mapped[str] = mapped_column(
        String(150), nullable=False, index=True
    )

    resource_type: Mapped[str] = mapped_column(
        String(80), nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    unit: Mapped[str] = mapped_column(
        String(30), nullable=False
    )

    price_per_unit: Mapped[float] = mapped_column(
        Float, nullable=False
    )

    available_quantity: Mapped[float] = mapped_column(
        Float, nullable=False, default=0
    )

    is_available: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )
