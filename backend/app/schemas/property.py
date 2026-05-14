from pydantic import BaseModel, Field


class PropertyPayload(BaseModel):
    property_name: str = Field(alias="propertyName")
    address: str
    city: str
    state: str
    zip_code: str = Field(alias="zipCode")
    property_type: str = Field(alias="propertyType")
    bedrooms: int
    bathrooms: float
    area_sqft: int = Field(alias="areaSqft")
    year_built: int = Field(alias="yearBuilt")
    furnishing_status: str = Field(alias="furnishingStatus")
    floor_number: int = Field(alias="floorNumber")
    parking_spaces: int = Field(alias="parkingSpaces")
    parking_availability: str = Field(alias="parkingAvailability")
    has_gym: bool = Field(alias="hasGym")
    has_pool: bool = Field(alias="hasPool")
    pet_friendly: bool = Field(alias="petFriendly")
    gated_community: bool = Field(alias="gatedCommunity")
    nearby_metro_distance: float = Field(alias="nearbyMetroDistance")
    amenities: list[str] = []

    class Config:
        allow_population_by_field_name = True


class NeighborhoodPayload(BaseModel):
    school_quality_score: float = Field(alias="schoolQualityScore")
    flood_risk_score: float = Field(alias="floodRiskScore")
    transit_score: float = Field(alias="transitScore")
    road_noise_score: float = Field(alias="roadNoiseScore")
    neighborhood_appeal_score: float = Field(alias="neighborhoodAppealScore")

    class Config:
        allow_population_by_field_name = True
