from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.analysis import AnalysisCreateRequest, AnalysisRecalculateRequest
from app.schemas.pricing import (
    FeedbackRequest,
    FeedbackResponse,
    RecommendationRequest,
    RecommendationResponse,
)
from app.services.analysis_service import AnalysisService

router = APIRouter(prefix="/pricing", tags=["pricing"])

@router.post("/recommendation", response_model=RecommendationResponse)
async def create_recommendation(
    payload: RecommendationRequest, db: AsyncSession = Depends(get_db)
):
    analysis = await AnalysisService(db).create_analysis(AnalysisCreateRequest(**payload.dict()))
    current = analysis.current_recommendation
    return RecommendationResponse(
        recommendation_id=101,
        recommended_rent=current.recommended_rent,
        rent_low=current.rent_low,
        rent_high=current.rent_high,
        confidence_score=current.confidence_score,
        price_per_sqft=current.price_per_sqft,
        reasoning_summary=current.reasoning_summary,
        market_trend_indicator=current.market_trend_indicator,
        pricing_factors=current.pricing_factors,
        neighborhood_summary=current.neighborhood_summary,
        comparables=[],
    )


@router.post("/recommend", response_model=RecommendationResponse)
async def recommend(payload: RecommendationRequest, db: AsyncSession = Depends(get_db)):
    return await create_recommendation(payload, db)


@router.post("/comparables", response_model=list[dict])
async def rank_comparables(payload: RecommendationRequest, db: AsyncSession = Depends(get_db)):
    response = await create_recommendation(payload, db)
    return [item.dict() for item in response.comparables]


@router.post("/feedback", response_model=FeedbackResponse)
async def process_feedback(payload: FeedbackRequest):
    return FeedbackResponse(
        updated_recommendation=RecommendationResponse(
            recommendation_id=0,
            recommended_rent=0,
            rent_low=0,
            rent_high=0,
            confidence_score=0,
            price_per_sqft=0,
            reasoning_summary="Use persistent analysis endpoints instead.",
            market_trend_indicator="No-op compatibility response.",
            pricing_factors=[],
            neighborhood_summary=[],
            comparables=[],
        ),
        parsed_intent="compatibility-only",
        pricing_adjustment=0,
    )


@router.post("/update", response_model=FeedbackResponse)
async def update_recommendation(payload: AnalysisRecalculateRequest):
    return FeedbackResponse(
        updated_recommendation=RecommendationResponse(
            recommendation_id=0,
            recommended_rent=0,
            rent_low=0,
            rent_high=0,
            confidence_score=0,
            price_per_sqft=0,
            reasoning_summary="Use /api/v1/analyses/{id}/recalculate instead.",
            market_trend_indicator="Compatibility response.",
            pricing_factors=[],
            neighborhood_summary=[],
            comparables=[],
        ),
        parsed_intent="compatibility-only",
        pricing_adjustment=0,
    )
