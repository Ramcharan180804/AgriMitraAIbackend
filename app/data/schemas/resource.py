from pydantic import BaseModel, ConfigDict, Field


class ResourceCreate(BaseModel):
    resource_name: str = Field(min_length=1, max_length=150)
    resource_type: str = Field(min_length=1, max_length=80)
    description: str | None = None
    unit: str = Field(min_length=1, max_length=30)
    price_per_unit: float = Field(ge=0)
    available_quantity: float = Field(default=0, ge=0)
    is_available: bool = True


class ResourceUpdate(BaseModel):
    resource_name: str | None = Field(default=None, min_length=1, max_length=150)
    resource_type: str | None = Field(default=None, min_length=1, max_length=80)
    description: str | None = None
    unit: str | None = Field(default=None, min_length=1, max_length=30)
    price_per_unit: float | None = Field(default=None, ge=0)
    available_quantity: float | None = Field(default=None, ge=0)
    is_available: bool | None = None


class ResourceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    resource_name: str
    resource_type: str
    description: str | None
    unit: str
    price_per_unit: float
    available_quantity: float
    is_available: bool
