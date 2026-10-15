from sqlalchemy import ForeignKey, Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.data.database.models import Base


class Farm(Base):
    __tablename__ = "farms"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    farm_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    location: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    district: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    village: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    area_acres: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    farmer_id: Mapped[int] = mapped_column(
        ForeignKey("farmers.id"),
        nullable=False,
        index=True,
    )

    farmer = relationship("Farmer")
