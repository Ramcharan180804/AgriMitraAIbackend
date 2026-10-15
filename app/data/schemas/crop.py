from pydantic import BaseModel, ConfigDict, Field, model_validator


class CropCreate(BaseModel):
    crop_name: str = Field(..., min_length=2, max_length=100)
    scientific_name: str | None = Field(default=None, max_length=150)
    crop_type: str | None = Field(default=None, max_length=100)
    suitable_soil: str | None = Field(default=None, max_length=150)

    min_temperature: float | None = None
    max_temperature: float | None = None
    min_rainfall: float | None = Field(default=None, ge=0)
    max_rainfall: float | None = Field(default=None, ge=0)

    description: str | None = None

    @model_validator(mode="after")
    def validate_ranges(self):
        if (
            self.min_temperature is not None
            and self.max_temperature is not None
            and self.min_temperature > self.max_temperature
        ):
            raise ValueError(
                "min_temperature cannot exceed max_temperature"
            )

        if (
            self.min_rainfall is not None
            and self.max_rainfall is not None
            and self.min_rainfall > self.max_rainfall
        ):
            raise ValueError(
                "min_rainfall cannot exceed max_rainfall"
            )

        return self


class CropUpdate(BaseModel):
    crop_name: str | None = Field(default=None, min_length=2, max_length=100)
    scientific_name: str | None = Field(default=None, max_length=150)
    crop_type: str | None = Field(default=None, max_length=100)
    suitable_soil: str | None = Field(default=None, max_length=150)

    min_temperature: float | None = None
    max_temperature: float | None = None
    min_rainfall: float | None = Field(default=None, ge=0)
    max_rainfall: float | None = Field(default=None, ge=0)

    description: str | None = None
    is_active: bool | None = None


class CropResponse(BaseModel):
    id: int
    crop_name: str
    scientific_name: str | None = None
    crop_type: str | None = None
    suitable_soil: str | None = None
    min_temperature: float | None = None
    max_temperature: float | None = None
    min_rainfall: float | None = None
    max_rainfall: float | None = None
    description: str | None = None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
