from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DiseaseDetectionCreate(BaseModel):
    farm_id: int = Field(gt=0)
    crop_id: int | None = Field(default=None, gt=0)

    image_path: str | None = Field(default=None, max_length=500)
    disease_name: str = Field(min_length=1, max_length=150)
    confidence_score: float | None = Field(default=None, ge=0, le=1)

    symptoms: str | None = None
    recommended_treatment: str | None = None


class DiseaseDetectionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    farm_id: int
    crop_id: int | None
    image_path: str | None
    disease_name: str
    confidence_score: float | None
    symptoms: str | None
    recommended_treatment: str | None
    detected_at: datetime
