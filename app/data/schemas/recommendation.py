from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RecommendationCreate(BaseModel):
    farm_id: int = Field(gt=0)
    crop_id: int = Field(gt=0)
    confidence_score: float | None = Field(default=None, ge=0, le=1)
    recommendation_reason: str | None = None
    season: str | None = Field(default=None, max_length=50)


class RecommendationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    farm_id: int
    crop_id: int
    confidence_score: float | None
    recommendation_reason: str | None
    season: str | None
    created_at: datetime
