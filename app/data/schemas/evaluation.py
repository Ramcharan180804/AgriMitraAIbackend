from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)


class EvaluationCreate(BaseModel):
    farm_id: int = Field(gt=0)
    crop_name: str = Field(min_length=1, max_length=100)
    yield_quantity: float = Field(ge=0)
    quality_rating: float = Field(ge=0, le=10)
    total_cost: float = Field(default=0, ge=0)
    profit: float | None = None
    notes: str | None = None

    @field_validator("crop_name")
    @classmethod
    def validate_crop_name(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("Crop name cannot be empty.")
        return value


class EvaluationUpdate(BaseModel):
    crop_name: str | None = Field(default=None, min_length=1, max_length=100)
    yield_quantity: float | None = Field(default=None, ge=0)
    quality_rating: float | None = Field(default=None, ge=0, le=10)
    total_cost: float | None = Field(default=None, ge=0)
    profit: float | None = None
    notes: str | None = None

    @field_validator("crop_name")
    @classmethod
    def validate_crop_name(cls, value):
        if value is not None:
            value = value.strip()
            if not value:
                raise ValueError("Crop name cannot be empty.")
        return value


class EvaluationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    farm_id: int
    crop_name: str
    yield_quantity: float
    quality_rating: float
    total_cost: float
    profit: float | None
    notes: str | None
    evaluated_at: datetime
