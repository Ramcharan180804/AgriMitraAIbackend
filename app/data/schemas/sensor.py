from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SensorReadingCreate(BaseModel):
    farm_id: int = Field(..., gt=0)
    sensor_type: str = Field(..., min_length=2, max_length=50)
    value: float
    unit: str = Field(..., min_length=1, max_length=20)
    recorded_at: datetime | None = None


class SensorReadingResponse(BaseModel):
    id: int
    farm_id: int
    sensor_type: str
    value: float
    unit: str
    recorded_at: datetime

    model_config = ConfigDict(from_attributes=True)
