from pydantic import BaseModel, ConfigDict, Field


class FarmCreate(BaseModel):
    farm_name: str = Field(..., min_length=2, max_length=150)
    area_acres: float = Field(..., gt=0)
    farmer_id: int = Field(..., gt=0)
    location: str | None = Field(default=None, max_length=255)
    district: str | None = Field(default=None, max_length=100)
    village: str | None = Field(default=None, max_length=100)


class FarmUpdate(BaseModel):
    farm_name: str | None = Field(default=None, min_length=2, max_length=150)
    area_acres: float | None = Field(default=None, gt=0)
    location: str | None = Field(default=None, max_length=255)
    district: str | None = Field(default=None, max_length=100)
    village: str | None = Field(default=None, max_length=100)


class FarmResponse(BaseModel):
    id: int
    farm_name: str
    area_acres: float
    farmer_id: int
    location: str | None = None
    district: str | None = None
    village: str | None = None

    model_config = ConfigDict(from_attributes=True)
