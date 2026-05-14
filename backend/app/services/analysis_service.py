from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.analysis_repository import AnalysisRepository
from app.schemas.analysis import (
    AnalysisCreateRequest,
    AnalysisDetailResponse,
    AnalysisFeedbackRequest,
    AnalysisListItemResponse,
    AnalysisListResponse,
    AnalysisRecalculateRequest,
    ComparableAdjustmentResponse,
    ComparableResponseModel,
    FeedbackMessageResponse,
    RecommendationEventResponse,
    RecommendationHistoryResponse,
    RecommendationSnapshotResponse,
)
from app.schemas.pricing import RecommendationRequest
from app.services.ai import GeminiService
from app.services.pricing_engine import (
    apply_comparable_actions,
    apply_feedback,
    build_recommendation,
)
from app.utils.serialization import dumps, loads


class AnalysisService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = AnalysisRepository(session)
        self.gemini = GeminiService()

    async def create_analysis(self, payload: AnalysisCreateRequest) -> AnalysisDetailResponse:
        property_record = await self.repository.create_property(
            property_name=payload.property.property_name,
            address=payload.property.address,
            city=payload.property.city,
            state=payload.property.state,
            zip_code=payload.property.zip_code,
            property_type=payload.property.property_type,
            bedrooms=payload.property.bedrooms,
            bathrooms=payload.property.bathrooms,
            area_sqft=payload.property.area_sqft,
            year_built=payload.property.year_built,
            furnishing_status=payload.property.furnishing_status,
            floor_number=payload.property.floor_number,
            parking_spaces=payload.property.parking_spaces,
            parking_availability=payload.property.parking_availability,
            has_gym=payload.property.has_gym,
            has_pool=payload.property.has_pool,
            pet_friendly=payload.property.pet_friendly,
            gated_community=payload.property.gated_community,
            nearby_metro_distance=payload.property.nearby_metro_distance,
            amenities_json=dumps(payload.property.amenities),
        )
        analysis = await self.repository.create_analysis(
            property_id=property_record.id,
            analyst_notes=payload.analyst_notes,
            status="active",
        )
        await self.repository.create_neighborhood_metrics(
            property_id=property_record.id,
            school_quality_score=payload.neighborhood.school_quality_score,
            flood_risk_score=payload.neighborhood.flood_risk_score,
            transit_score=payload.neighborhood.transit_score,
            road_noise_score=payload.neighborhood.road_noise_score,
            neighborhood_appeal_score=payload.neighborhood.neighborhood_appeal_score,
        )

        recommendation = build_recommendation(
            RecommendationRequest(
                property=payload.property,
                neighborhood=payload.neighborhood,
                analyst_notes=payload.analyst_notes,
            )
        )
        explanation = self.gemini.generate_recommendation_explanation(
            {
                "property": payload.property.dict(by_alias=True),
                "neighborhood": payload.neighborhood.dict(by_alias=True),
                "recommendation": recommendation.dict(),
                "analyst_notes": payload.analyst_notes,
            }
        )
        if explanation:
            recommendation.reasoning_summary = explanation
        rec_model = await self.repository.create_recommendation(
            analysis_id=analysis.id,
            version_number=1,
            recommended_rent=recommendation.recommended_rent,
            rent_low=recommendation.rent_low,
            rent_high=recommendation.rent_high,
            confidence_score=recommendation.confidence_score,
            price_per_sqft=recommendation.price_per_sqft,
            reasoning_summary=recommendation.reasoning_summary,
            market_trend_indicator=recommendation.market_trend_indicator,
            pricing_factors_json=dumps(recommendation.pricing_factors),
            neighborhood_summary_json=dumps(recommendation.neighborhood_summary),
            triggered_by="initial_generation",
        )
        for comparable in recommendation.comparables:
            await self.repository.create_comparable(
                recommendation_id=rec_model.id,
                property_name=comparable.property_name,
                address=comparable.address,
                monthly_rent=comparable.monthly_rent,
                bedrooms=comparable.bedrooms,
                bathrooms=comparable.bathrooms,
                area_sqft=comparable.area_sqft,
                distance_miles=comparable.distance_miles,
                similarity_score=comparable.similarity_score,
                match_percentage=comparable.match_percentage,
                selection_reason=comparable.selection_reason,
                key_matching_factors_json=dumps(comparable.key_matching_factors),
                weight=comparable.weight,
                status=comparable.status,
            )
        await self.repository.set_latest_recommendation(analysis, rec_model)
        await self.repository.create_event(
            analysis_id=analysis.id,
            event_type="analysis_created",
            event_summary="Initial analysis generated and persisted.",
            metadata_json=dumps({"recommendation_version": 1}),
        )
        await self.session.commit()
        analysis = await self.repository.get_analysis(analysis.id)
        return self._serialize_analysis(analysis)

    async def list_analyses(
        self, page: int, page_size: int, city: str | None, property_type: str | None, search: str | None
    ) -> AnalysisListResponse:
        analyses, total = await self.repository.list_analyses(
            page=page, page_size=page_size, city=city, property_type=property_type, search=search
        )
        items = []
        for analysis in analyses:
            latest = await self.repository.get_latest_recommendation(analysis.id)
            items.append(
                AnalysisListItemResponse(
                    id=analysis.id,
                    property_name=analysis.property.property_name,
                    city=analysis.property.city,
                    property_type=analysis.property.property_type,
                    status=analysis.status,
                    latest_recommendation_value=latest.recommended_rent if latest else None,
                    latest_confidence_score=latest.confidence_score if latest else None,
                    updated_at=analysis.updated_at,
                )
            )
        return AnalysisListResponse(items=items, total=total, page=page, page_size=page_size)

    async def get_analysis(self, analysis_id: UUID) -> AnalysisDetailResponse:
        analysis = await self.repository.get_analysis(analysis_id)
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found")
        return self._serialize_analysis(analysis)

    async def add_feedback(
        self, analysis_id: UUID, payload: AnalysisFeedbackRequest
    ) -> AnalysisDetailResponse:
        return await self.recalculate_analysis(
            analysis_id,
            AnalysisRecalculateRequest(feedback_text=payload.feedback_text),
        )

    async def recalculate_analysis(
        self, analysis_id: UUID, payload: AnalysisRecalculateRequest
    ) -> AnalysisDetailResponse:
        analysis = await self.repository.get_analysis(analysis_id)
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found")
        previous = await self.repository.get_latest_recommendation(analysis_id)
        if not previous:
            raise HTTPException(status_code=404, detail="Recommendation not found")

        serialized_previous = self._serialize_recommendation(previous)
        next_recommendation = serialized_previous
        trigger_type = "manual_recalculation"
        parsed_intent = "manual refinement"
        pricing_adjustment = 0.0

        if payload.comparable_actions:
            next_recommendation = apply_comparable_actions(
                next_recommendation, payload.comparable_actions
            )
            trigger_type = "comparable_adjustment"
            for action in payload.comparable_actions:
                comparable = next(
                    (comp for comp in previous.comparables if comp.id == action.comparable_id), None
                )
                if comparable:
                    updated_comp = next(
                        (
                            comp
                            for comp in next_recommendation.comparables
                            if str(comp.id) == str(action.comparable_id)
                        ),
                        None,
                    )
                    await self.repository.create_adjustment(
                        comparable_property_id=comparable.id,
                        action=action.action,
                        previous_weight=comparable.weight,
                        new_weight=updated_comp.weight if updated_comp else comparable.weight,
                        previous_status=comparable.status,
                        new_status=updated_comp.status if updated_comp else comparable.status,
                        reason="Analyst comparable adjustment",
                    )

        if payload.feedback_text:
            ai_feedback = self.gemini.interpret_feedback(
                payload.feedback_text,
                {
                    "analysis_id": str(analysis.id),
                    "recommendation": next_recommendation.dict(),
                },
            )
            if ai_feedback:
                parsed_intent = ai_feedback.get("parsed_intent", parsed_intent)
                pricing_adjustment = float(ai_feedback.get("pricing_adjustment", 0))
                if pricing_adjustment:
                    next_recommendation = next_recommendation.copy(
                        update={
                            "recommended_rent": round(
                                next_recommendation.recommended_rent + pricing_adjustment, 2
                            ),
                            "rent_low": round(
                                (next_recommendation.recommended_rent + pricing_adjustment)
                                * 0.94,
                                2,
                            ),
                            "rent_high": round(
                                (next_recommendation.recommended_rent + pricing_adjustment)
                                * 1.07,
                                2,
                            ),
                            "reasoning_summary": (
                                ai_feedback.get("explanation")
                                or next_recommendation.reasoning_summary
                            ),
                        }
                    )
                if ai_feedback.get("comparable_actions"):
                    from app.schemas.pricing import ComparableAction

                    comparable_actions = [
                        ComparableAction(**item)
                        for item in ai_feedback["comparable_actions"]
                        if isinstance(item, dict)
                    ]
                    if comparable_actions:
                        next_recommendation = apply_comparable_actions(
                            next_recommendation, comparable_actions
                        )
            else:
                next_recommendation, parsed_intent, pricing_adjustment = apply_feedback(
                    next_recommendation, payload.feedback_text
                )
            trigger_type = "feedback_update"
            await self.repository.create_feedback(
                analysis_id=analysis.id,
                recommendation_id=previous.id,
                role="analyst",
                message_text=payload.feedback_text,
                parsed_intent=parsed_intent,
                pricing_adjustment=pricing_adjustment,
                affected_recommendation_version=previous.version_number,
            )
            explanation = self.gemini.generate_recommendation_explanation(
                {
                    "analysis_id": str(analysis.id),
                    "feedback": payload.feedback_text,
                    "recommendation": next_recommendation.dict(),
                }
            )
            if explanation:
                next_recommendation = next_recommendation.copy(
                    update={"reasoning_summary": explanation}
                )
            await self.repository.create_feedback(
                analysis_id=analysis.id,
                recommendation_id=previous.id,
                role="assistant",
                message_text=f'Recommendation updated after "{parsed_intent}".',
                parsed_intent=parsed_intent,
                pricing_adjustment=pricing_adjustment,
                affected_recommendation_version=previous.version_number + 1,
            )

        new_rec = await self.repository.create_recommendation(
            analysis_id=analysis.id,
            version_number=previous.version_number + 1,
            recommended_rent=next_recommendation.recommended_rent,
            rent_low=next_recommendation.rent_low,
            rent_high=next_recommendation.rent_high,
            confidence_score=next_recommendation.confidence_score,
            price_per_sqft=next_recommendation.price_per_sqft,
            reasoning_summary=next_recommendation.reasoning_summary,
            market_trend_indicator=next_recommendation.market_trend_indicator,
            pricing_factors_json=dumps(next_recommendation.pricing_factors),
            neighborhood_summary_json=dumps(next_recommendation.neighborhood_summary),
            triggered_by=trigger_type,
        )
        for comparable in next_recommendation.comparables:
            await self.repository.create_comparable(
                recommendation_id=new_rec.id,
                property_name=comparable.property_name,
                address=comparable.address,
                monthly_rent=comparable.monthly_rent,
                bedrooms=comparable.bedrooms,
                bathrooms=comparable.bathrooms,
                area_sqft=comparable.area_sqft,
                distance_miles=comparable.distance_miles,
                similarity_score=comparable.similarity_score,
                match_percentage=comparable.match_percentage,
                selection_reason=comparable.selection_reason,
                key_matching_factors_json=dumps(comparable.key_matching_factors),
                weight=comparable.weight,
                status=comparable.status,
            )
        await self.repository.create_history(
            analysis_id=analysis.id,
            recommendation_id=new_rec.id,
            previous_recommendation_value=previous.recommended_rent,
            new_recommendation_value=new_rec.recommended_rent,
            previous_confidence_score=previous.confidence_score,
            new_confidence_score=new_rec.confidence_score,
            change_reason=parsed_intent if payload.feedback_text else "Comparable set changed",
            trigger_type=trigger_type,
        )
        await self.repository.create_event(
            analysis_id=analysis.id,
            event_type=trigger_type,
            event_summary="Recommendation recalculated and persisted.",
            metadata_json=dumps(
                {
                    "from_version": previous.version_number,
                    "to_version": new_rec.version_number,
                    "pricing_adjustment": pricing_adjustment,
                }
            ),
        )
        await self.repository.set_latest_recommendation(analysis, new_rec)
        await self.session.commit()
        refreshed = await self.repository.get_analysis(analysis.id)
        return self._serialize_analysis(refreshed)

    async def get_history(self, analysis_id: UUID) -> list[RecommendationHistoryResponse]:
        analysis = await self.repository.get_analysis(analysis_id)
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found")
        history = []
        for recommendation in analysis.recommendations:
            for item in recommendation.history_entries:
                history.append(
                    RecommendationHistoryResponse(
                        id=item.id,
                        recommendation_id=item.recommendation_id,
                        previous_recommendation_value=item.previous_recommendation_value,
                        new_recommendation_value=item.new_recommendation_value,
                        previous_confidence_score=item.previous_confidence_score,
                        new_confidence_score=item.new_confidence_score,
                        change_reason=item.change_reason,
                        trigger_type=item.trigger_type,
                        created_at=item.created_at,
                    )
                )
        return sorted(history, key=lambda item: item.created_at)

    def _serialize_analysis(self, analysis) -> AnalysisDetailResponse:
        recommendations = sorted(analysis.recommendations, key=lambda item: item.version_number)
        current = recommendations[-1] if recommendations else None
        history = []
        for recommendation in recommendations:
            for item in recommendation.history_entries:
                history.append(
                    RecommendationHistoryResponse(
                        id=item.id,
                        recommendation_id=item.recommendation_id,
                        previous_recommendation_value=item.previous_recommendation_value,
                        new_recommendation_value=item.new_recommendation_value,
                        previous_confidence_score=item.previous_confidence_score,
                        new_confidence_score=item.new_confidence_score,
                        change_reason=item.change_reason,
                        trigger_type=item.trigger_type,
                        created_at=item.created_at,
                    )
                )
        events = [
            RecommendationEventResponse(
                id=event.id,
                event_type=event.event_type,
                event_summary=event.event_summary,
                metadata=loads(event.metadata_json, {}),
                created_at=event.created_at,
            )
            for event in sorted(analysis.events, key=lambda item: item.created_at)
        ]
        feedback = [
            FeedbackMessageResponse(
                id=message.id,
                role=message.role,
                message_text=message.message_text,
                parsed_intent=message.parsed_intent,
                pricing_adjustment=message.pricing_adjustment,
                affected_recommendation_version=message.affected_recommendation_version,
                created_at=message.created_at,
            )
            for message in sorted(analysis.feedback_messages, key=lambda item: item.created_at)
        ]
        return AnalysisDetailResponse(
            id=analysis.id,
            property_name=analysis.property.property_name,
            address=analysis.property.address,
            city=analysis.property.city,
            state=analysis.property.state,
            zip_code=analysis.property.zip_code,
            property_type=analysis.property.property_type,
            status=analysis.status,
            analyst_notes=analysis.analyst_notes,
            amenities=loads(analysis.property.amenities_json, []),
            current_recommendation=self._serialize_recommendation(current) if current else None,
            feedback_messages=feedback,
            recommendation_history=sorted(history, key=lambda item: item.created_at),
            recommendation_events=events,
        )

    def _serialize_recommendation(self, recommendation) -> RecommendationSnapshotResponse:
        return RecommendationSnapshotResponse(
            id=recommendation.id,
            version_number=recommendation.version_number,
            recommended_rent=recommendation.recommended_rent,
            rent_low=recommendation.rent_low,
            rent_high=recommendation.rent_high,
            confidence_score=recommendation.confidence_score,
            price_per_sqft=recommendation.price_per_sqft,
            reasoning_summary=recommendation.reasoning_summary,
            market_trend_indicator=recommendation.market_trend_indicator,
            pricing_factors=loads(recommendation.pricing_factors_json, []),
            neighborhood_summary=loads(recommendation.neighborhood_summary_json, []),
            triggered_by=recommendation.triggered_by,
            created_at=recommendation.created_at,
            comparables=[
                ComparableResponseModel(
                    id=item.id,
                    property_name=item.property_name,
                    address=item.address,
                    monthly_rent=item.monthly_rent,
                    bedrooms=item.bedrooms,
                    bathrooms=item.bathrooms,
                    area_sqft=item.area_sqft,
                    distance_miles=item.distance_miles,
                    similarity_score=item.similarity_score,
                    match_percentage=item.match_percentage,
                    selection_reason=item.selection_reason,
                    key_matching_factors=loads(item.key_matching_factors_json, []),
                    weight=item.weight,
                    status=item.status,
                    adjustments=[
                        ComparableAdjustmentResponse(
                            id=adj.id,
                            action=adj.action,
                            previous_weight=adj.previous_weight,
                            new_weight=adj.new_weight,
                            previous_status=adj.previous_status,
                            new_status=adj.new_status,
                            created_at=adj.created_at,
                        )
                        for adj in sorted(item.adjustments, key=lambda value: value.created_at)
                    ],
                )
                for item in recommendation.comparables
            ],
        )
