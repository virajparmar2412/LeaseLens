from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.pricing import ComparableAction, RecommendationRequest


class AnalysisCreateRequest(RecommendationRequest):
    pass


class AnalysisFeedbackRequest(BaseModel):
    feedback_text: str


class AnalysisRecalculateRequest(BaseModel):
    feedback_text: str | None = None
    comparable_actions: list[ComparableAction] = Field(default_factory=list)


class ComparableAdjustmentResponse(BaseModel):
    id: UUID
    action: str
    previous_weight: float
    new_weight: float
    previous_status: str
    new_status: str
    created_at: datetime


class ComparableResponseModel(BaseModel):
    id: UUID
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
    weight: float
    status: str
    adjustments: list[ComparableAdjustmentResponse] = []


class FeedbackMessageResponse(BaseModel):
    id: UUID
    role: str
    message_text: str
    parsed_intent: str
    pricing_adjustment: float
    affected_recommendation_version: int
    created_at: datetime


class RecommendationSnapshotResponse(BaseModel):
    id: UUID
    version_number: int
    recommended_rent: float
    rent_low: float
    rent_high: float
    confidence_score: float
    price_per_sqft: float
    reasoning_summary: str
    market_trend_indicator: str
    pricing_factors: list[dict]
    neighborhood_summary: list[dict]
    triggered_by: str
    created_at: datetime
    comparables: list[ComparableResponseModel]


class RecommendationHistoryResponse(BaseModel):
    id: UUID
    recommendation_id: UUID
    previous_recommendation_value: float
    new_recommendation_value: float
    previous_confidence_score: float
    new_confidence_score: float
    change_reason: str
    trigger_type: str
    created_at: datetime


class RecommendationEventResponse(BaseModel):
    id: UUID
    event_type: str
    event_summary: str
    metadata: dict
    created_at: datetime


class AnalysisListItemResponse(BaseModel):
    id: UUID
    property_name: str
    city: str
    property_type: str
    status: str
    latest_recommendation_value: float | None
    latest_confidence_score: float | None
    updated_at: datetime


class AnalysisDetailResponse(BaseModel):
    id: UUID
    property_name: str
    address: str
    city: str
    state: str
    zip_code: str
    property_type: str
    status: str
    analyst_notes: str | None
    amenities: list[str]
    current_recommendation: RecommendationSnapshotResponse | None
    feedback_messages: list[FeedbackMessageResponse]
    recommendation_history: list[RecommendationHistoryResponse]
    recommendation_events: list[RecommendationEventResponse]


class AnalysisListResponse(BaseModel):
    items: list[AnalysisListItemResponse]
    total: int
    page: int
    page_size: int
