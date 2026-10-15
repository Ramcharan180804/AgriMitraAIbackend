from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class BookingCreate(BaseModel):
    farmer_id: int = Field(gt=0)
    resource_id: int = Field(gt=0)
    quantity: float = Field(gt=0)
    notes: str | None = None


class BookingStatusUpdate(BaseModel):
    booking_status: str = Field(
        pattern=r"^(PENDING|CONFIRMED|CANCELLED|COMPLETED)$"
    )


class BookingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    farmer_id: int
    resource_id: int
    quantity: float
    total_price: float
    booking_status: str
    booking_date: datetime
    notes: str | None
