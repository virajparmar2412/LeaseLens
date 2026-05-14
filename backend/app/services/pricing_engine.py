from app.schemas.pricing import (
    ComparableAction,
    ComparableResponse,
    RecommendationRequest,
    RecommendationResponse,
)

WEIGHTS = {
    "location": 0.25,
    "area": 0.15,
    "amenities": 0.10,
    "school_quality": 0.10,
    "flood_risk": 0.05,
    "transit": 0.10,
    "road_noise": 0.05,
    "neighborhood_appeal": 0.10,
    "rental_history": 0.10,
}


def _mock_comparables(subject: RecommendationRequest) -> list[ComparableResponse]:
    sqft = subject.property.area_sqft
    return [
        ComparableResponse(
            id=1,
            property_name="Harbor Crest Residences",
            address="214 Harbor Crest Ave",
            monthly_rent=round((sqft * 2.1) + 120, 2),
            bedrooms=subject.property.bedrooms,
            bathrooms=subject.property.bathrooms,
            area_sqft=sqft - 45,
            distance_miles=0.6,
            similarity_score=0.92,
            match_percentage=92.0,
            selection_reason="Very close in size, beds/baths, and neighborhood demand profile.",
            key_matching_factors=["size alignment", "transit access", "amenity overlap"],
        ),
        ComparableResponse(
            id=2,
            property_name="Westline Residences",
            address="78 Westline Residences",
            monthly_rent=round((sqft * 2.0) + 80, 2),
            bedrooms=subject.property.bedrooms,
            bathrooms=subject.property.bathrooms,
            area_sqft=sqft + 35,
            distance_miles=0.9,
            similarity_score=0.88,
            match_percentage=88.0,
            selection_reason="Strong amenity overlap with slightly lower transit convenience.",
            key_matching_factors=["school quality", "parking availability", "premium finishes"],
        ),
        ComparableResponse(
            id=3,
            property_name="Cedar Point Lofts",
            address="355 Cedar Point Lofts",
            monthly_rent=round((sqft * 2.15) + 40, 2),
            bedrooms=subject.property.bedrooms + 1,
            bathrooms=subject.property.bathrooms,
            area_sqft=sqft + 75,
            distance_miles=1.2,
            similarity_score=0.84,
            match_percentage=84.0,
            selection_reason="Useful upper-bound comp due to larger footprint and premium finish set.",
            key_matching_factors=["premium positioning", "newer inventory", "appeal score"],
        ),
    ]


def build_recommendation(payload: RecommendationRequest) -> RecommendationResponse:
    area_score = min(payload.property.area_sqft / 1500, 1)
    amenity_score = (
        int(payload.property.has_gym)
        + int(payload.property.has_pool)
        + int(payload.property.pet_friendly)
    ) / 3
    neighborhood = payload.neighborhood

    composite_score = (
        WEIGHTS["location"] * 0.82
        + WEIGHTS["area"] * area_score
        + WEIGHTS["amenities"] * amenity_score
        + WEIGHTS["school_quality"] * (neighborhood.school_quality_score / 10)
        + WEIGHTS["flood_risk"] * (1 - (neighborhood.flood_risk_score / 10))
        + WEIGHTS["transit"] * (neighborhood.transit_score / 10)
        + WEIGHTS["road_noise"] * (1 - (neighborhood.road_noise_score / 10))
        + WEIGHTS["neighborhood_appeal"] * (neighborhood.neighborhood_appeal_score / 10)
        + WEIGHTS["rental_history"] * 0.8
    )

    local_price_benchmark = 2.15
    recommended_rent = round(payload.property.area_sqft * local_price_benchmark * composite_score, 2)
    rent_low = round(recommended_rent * 0.94, 2)
    rent_high = round(recommended_rent * 1.07, 2)
    confidence_score = round(min(0.62 + (composite_score * 0.3), 0.96), 2)

    return RecommendationResponse(
        recommendation_id=101,
        recommended_rent=recommended_rent,
        rent_low=rent_low,
        rent_high=rent_high,
        confidence_score=confidence_score,
        price_per_sqft=round(recommended_rent / max(payload.property.area_sqft, 1), 2),
        reasoning_summary="Recommendation balances property signals, neighborhood metrics, and comparable rental history.",
        market_trend_indicator="Demand trending upward in this submarket over the last 90 days.",
        pricing_factors=[
            {"name": "Location", "value": 82},
            {"name": "Amenities", "value": round(amenity_score * 100, 0)},
            {"name": "Transit", "value": round(neighborhood.transit_score * 10, 0)},
            {"name": "School Quality", "value": round(neighborhood.school_quality_score * 10, 0)},
            {"name": "Neighborhood Appeal", "value": round(neighborhood.neighborhood_appeal_score * 10, 0)},
        ],
        neighborhood_summary=[
            {"label": "School Rating", "score": neighborhood.school_quality_score},
            {"label": "Transit Access", "score": neighborhood.transit_score},
            {"label": "Road Noise", "score": 10 - neighborhood.road_noise_score},
            {"label": "Flood Resilience", "score": 10 - neighborhood.flood_risk_score},
            {"label": "Neighborhood Appeal", "score": neighborhood.neighborhood_appeal_score},
        ],
        comparables=_mock_comparables(payload),
    )


def apply_feedback(
    recommendation: RecommendationResponse, feedback_text: str
) -> tuple[RecommendationResponse, str, float]:
    normalized = feedback_text.lower()
    adjustment = 0.0
    intent = "neutral review"

    if "too low" in normalized or "raise" in normalized:
        adjustment = 125.0
        intent = "increase rent"
    elif "too high" in normalized or "lower" in normalized:
        adjustment = -125.0
        intent = "decrease rent"
    elif "luxury" in normalized or "premium" in normalized:
        adjustment = 175.0
        intent = "premium adjustment"

    updated_rent = round(recommendation.recommended_rent + adjustment, 2)
    updated = recommendation.copy(
        update={
            "recommended_rent": updated_rent,
            "rent_low": round(updated_rent * 0.94, 2),
            "rent_high": round(updated_rent * 1.07, 2),
            "confidence_score": round(
                max(0.55, min(0.97, recommendation.confidence_score + (adjustment / 2500))), 2
            ),
            "reasoning_summary": recommendation.reasoning_summary
            + " Analyst feedback was incorporated into the adjusted range.",
        }
    )
    return updated, intent, adjustment


def apply_comparable_actions(
    recommendation: RecommendationResponse, actions: list[ComparableAction]
) -> RecommendationResponse:
    comparables = [comp.copy() for comp in recommendation.comparables]
    rent_adjustment = 0.0
    confidence_adjustment = 0.0

    for action in actions:
        for comparable in comparables:
            if comparable.id != action.comparable_id:
                continue
            if action.action == "remove":
                comparable.status = "removed"
                rent_adjustment -= 45
                confidence_adjustment -= 0.03
            elif action.action == "increase_weight":
                comparable.weight = round(comparable.weight + 0.15, 2)
                rent_adjustment += 35
                confidence_adjustment += 0.01
            elif action.action == "decrease_weight":
                comparable.weight = max(0.2, round(comparable.weight - 0.15, 2))
                rent_adjustment -= 25
            elif action.action == "mark_irrelevant":
                comparable.status = "irrelevant"
                comparable.weight = 0.0
                rent_adjustment -= 60
                confidence_adjustment -= 0.04

    updated_rent = round(recommendation.recommended_rent + rent_adjustment, 2)
    active_comparables = [comp for comp in comparables if comp.status == "active"]
    updated_reasoning = recommendation.reasoning_summary + " Comparable analyst actions were reflected in the pricing band."

    return recommendation.copy(
        update={
            "recommended_rent": updated_rent,
            "rent_low": round(updated_rent * 0.94, 2),
            "rent_high": round(updated_rent * 1.07, 2),
            "confidence_score": round(
                max(0.45, min(0.97, recommendation.confidence_score + confidence_adjustment)),
                2,
            ),
            "reasoning_summary": updated_reasoning,
            "comparables": active_comparables + [comp for comp in comparables if comp.status != "active"],
        }
    )
