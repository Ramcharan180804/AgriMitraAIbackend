from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class FarmingActivityCreate(BaseModel):
    farm_id: int = Field(gt=0)
    activity_type: str = Field(min_length=1, max_length=100)
    description: str | None = None
    resource_used: str | None = Field(default=None, max_length=150)
    quantity_used: float | None = Field(default=None, ge=0)
    cost: float = Field(default=0, ge=0)
    notes: str | None = None

    @field_validator("activity_type")
    @classmethod
    def validate_activity_type(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("Activity type cannot be empty.")
        return value


class FarmingActivityUpdate(BaseModel):
    activity_type: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    resource_used: str | None = Field(default=None, max_length=150)
    quantity_used: float | None = Field(default=None, ge=0)
    cost: float | None = Field(default=None, ge=0)
    notes: str | None = None

    @field_validator("activity_type")
    @classmethod
    def validate_activity_type(cls, value):
        if value is not None:
            value = value.strip()
            if not value:
                raise ValueError("Activity type cannot be empty.")
        return value


class FarmingActivityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    farm_id: int
    activity_type: str
    activity_date: datetime
    description: str | None
    resource_used: str | None
    quantity_used: float | None
    cost: float
    notes: str | None
