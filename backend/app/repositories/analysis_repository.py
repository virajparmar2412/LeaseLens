from __future__ import annotations

from typing import Sequence
from uuid import UUID

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import (
    AnalystFeedback,
    ComparableAdjustment,
    ComparableProperty,
    NeighborhoodMetric,
    PricingRecommendation,
    Property,
    PropertyAnalysis,
    RecommendationEvent,
    RecommendationHistory,
)


class AnalysisRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_property(self, **kwargs) -> Property:
        property_record = Property(**kwargs)
        self.session.add(property_record)
        await self.session.flush()
        return property_record

    async def create_analysis(self, **kwargs) -> PropertyAnalysis:
        analysis = PropertyAnalysis(**kwargs)
        self.session.add(analysis)
        await self.session.flush()
        return analysis

    async def create_neighborhood_metrics(self, **kwargs) -> NeighborhoodMetric:
        metrics = NeighborhoodMetric(**kwargs)
        self.session.add(metrics)
        await self.session.flush()
        return metrics

    async def create_recommendation(self, **kwargs) -> PricingRecommendation:
        recommendation = PricingRecommendation(**kwargs)
        self.session.add(recommendation)
        await self.session.flush()
        return recommendation

    async def create_comparable(self, **kwargs) -> ComparableProperty:
        comparable = ComparableProperty(**kwargs)
        self.session.add(comparable)
        await self.session.flush()
        return comparable

    async def create_feedback(self, **kwargs) -> AnalystFeedback:
        feedback = AnalystFeedback(**kwargs)
        self.session.add(feedback)
        await self.session.flush()
        return feedback

    async def create_adjustment(self, **kwargs) -> ComparableAdjustment:
        adjustment = ComparableAdjustment(**kwargs)
        self.session.add(adjustment)
        await self.session.flush()
        return adjustment

    async def create_history(self, **kwargs) -> RecommendationHistory:
        history = RecommendationHistory(**kwargs)
        self.session.add(history)
        await self.session.flush()
        return history

    async def create_event(self, **kwargs) -> RecommendationEvent:
        event = RecommendationEvent(**kwargs)
        self.session.add(event)
        await self.session.flush()
        return event

    async def set_latest_recommendation(
        self, analysis: PropertyAnalysis, recommendation: PricingRecommendation
    ) -> None:
        analysis.latest_recommendation_id = recommendation.id
        await self.session.flush()

    async def get_analysis(self, analysis_id: UUID) -> PropertyAnalysis | None:
        query = (
            select(PropertyAnalysis)
            .where(PropertyAnalysis.id == analysis_id)
            .options(
                selectinload(PropertyAnalysis.property),
                selectinload(PropertyAnalysis.feedback_messages),
                selectinload(PropertyAnalysis.events),
                selectinload(PropertyAnalysis.recommendations)
                .selectinload(PricingRecommendation.comparables)
                .selectinload(ComparableProperty.adjustments),
                selectinload(PropertyAnalysis.recommendations)
                .selectinload(PricingRecommendation.history_entries),
            )
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_latest_recommendation(
        self, analysis_id: UUID
    ) -> PricingRecommendation | None:
        query = (
            select(PricingRecommendation)
            .where(PricingRecommendation.analysis_id == analysis_id)
            .order_by(PricingRecommendation.version_number.desc())
            .options(
                selectinload(PricingRecommendation.comparables).selectinload(
                    ComparableProperty.adjustments
                )
            )
            .limit(1)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_comparable(self, comparable_id: UUID) -> ComparableProperty | None:
        result = await self.session.execute(
            select(ComparableProperty).where(ComparableProperty.id == comparable_id)
        )
        return result.scalar_one_or_none()

    async def list_analyses(
        self,
        page: int,
        page_size: int,
        city: str | None = None,
        property_type: str | None = None,
        search: str | None = None,
    ) -> tuple[Sequence[PropertyAnalysis], int]:
        query: Select[tuple[PropertyAnalysis]] = (
            select(PropertyAnalysis)
            .join(Property)
            .options(selectinload(PropertyAnalysis.property))
            .order_by(PropertyAnalysis.updated_at.desc())
        )
        count_query = select(func.count(PropertyAnalysis.id)).join(Property)

        if city:
            query = query.where(Property.city.ilike(f"%{city}%"))
            count_query = count_query.where(Property.city.ilike(f"%{city}%"))
        if property_type:
            query = query.where(Property.property_type == property_type)
            count_query = count_query.where(Property.property_type == property_type)
        if search:
            query = query.where(Property.property_name.ilike(f"%{search}%"))
            count_query = count_query.where(Property.property_name.ilike(f"%{search}%"))

        total = (await self.session.execute(count_query)).scalar_one()
        items = (
            await self.session.execute(
                query.offset((page - 1) * page_size).limit(page_size)
            )
        ).scalars().all()
        return items, total
