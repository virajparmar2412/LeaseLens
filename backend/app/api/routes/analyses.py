from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.analysis import (
    AnalysisCreateRequest,
    AnalysisDetailResponse,
    AnalysisFeedbackRequest,
    AnalysisListResponse,
    AnalysisRecalculateRequest,
    RecommendationHistoryResponse,
)
from app.services.analysis_service import AnalysisService

router = APIRouter(prefix="/analyses", tags=["analyses"])


@router.post("", response_model=AnalysisDetailResponse)
async def create_analysis(
    payload: AnalysisCreateRequest, db: AsyncSession = Depends(get_db)
):
    return await AnalysisService(db).create_analysis(payload)


@router.get("", response_model=AnalysisListResponse)
async def list_analyses(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
    city: str | None = None,
    property_type: str | None = None,
    search: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    return await AnalysisService(db).list_analyses(page, page_size, city, property_type, search)


@router.get("/{analysis_id}", response_model=AnalysisDetailResponse)
async def get_analysis(analysis_id: UUID, db: AsyncSession = Depends(get_db)):
    return await AnalysisService(db).get_analysis(analysis_id)


@router.post("/{analysis_id}/feedback", response_model=AnalysisDetailResponse)
async def add_feedback(
    analysis_id: UUID,
    payload: AnalysisFeedbackRequest,
    db: AsyncSession = Depends(get_db),
):
    return await AnalysisService(db).add_feedback(analysis_id, payload)


@router.post("/{analysis_id}/recalculate", response_model=AnalysisDetailResponse)
async def recalculate_analysis(
    analysis_id: UUID,
    payload: AnalysisRecalculateRequest,
    db: AsyncSession = Depends(get_db),
):
    return await AnalysisService(db).recalculate_analysis(analysis_id, payload)


@router.get("/{analysis_id}/history", response_model=list[RecommendationHistoryResponse])
async def get_analysis_history(
    analysis_id: UUID, db: AsyncSession = Depends(get_db)
):
    return await AnalysisService(db).get_history(analysis_id)
