from uuid import UUID

from pydantic import BaseModel

from app.schemas.property import NeighborhoodPayload, PropertyPayload


class RecommendationRequest(BaseModel):
    property: PropertyPayload
    neighborhood: NeighborhoodPayload
    analyst_notes: str | None = None


class ComparableResponse(BaseModel):
    id: int
    property_name: str
    address: str
    monthly_rent: float
    bedrooms: int
    bathrooms: float
    area_sqft: int
    distance_miles: float
    similarity_score: float
    match_percentage: float
    selection_reason: str
    key_matching_factors: list[str]
    weight: float = 1.0
    status: str = "active"


class RecommendationResponse(BaseModel):
    recommendation_id: int
    recommended_rent: float
    rent_low: float
    rent_high: float
    confidence_score: float
    price_per_sqft: float
    reasoning_summary: str
    market_trend_indicator: str
    pricing_factors: list[dict]
    neighborhood_summary: list[dict]
    comparables: list[ComparableResponse]


class FeedbackRequest(BaseModel):
    recommendation_id: int
    feedback_text: str


class ComparableAction(BaseModel):
    comparable_id: UUID | int
    action: str


class RecommendationUpdateRequest(BaseModel):
    recommendation_id: int
    feedback_text: str | None = None
    comparable_actions: list[ComparableAction] = []


class FeedbackResponse(BaseModel):
    updated_recommendation: RecommendationResponse
    parsed_intent: str
    pricing_adjustment: float
