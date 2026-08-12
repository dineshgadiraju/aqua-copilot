from pydantic import BaseModel, Field


class PondCreate(BaseModel):
    pond_name: str = Field(
        ...,
        min_length=1,
        max_length=100
    )

    location: str | None = None

    area_m2: float | None = Field(
        default=None,
        gt=0
    )

    species: str = "Vannamei"


class PondReading(BaseModel):
    pond_name: str = "Pond 1"

    temperature_c: float = Field(
        ...,
        ge=15,
        le=45
    )

    ph: float = Field(
        ...,
        ge=4,
        le=11
    )

    dissolved_oxygen_mg_l: float = Field(
        ...,
        ge=0,
        le=20
    )

    salinity_ppt: float = Field(
        ...,
        ge=0,
        le=50
    )

    ammonia_mg_l: float = Field(
        ...,
        ge=0,
        le=5
    )

    feed_kg_day: float = Field(
        ...,
        ge=0,
        le=500
    )

    shrimp_age_days: int = Field(
        ...,
        ge=1,
        le=365
    )

    stocking_density_per_m2: float = Field(
        ...,
        ge=1,
        le=300
    )