import asyncio

from app.db.session import SessionLocal
from app.schemas.analysis import AnalysisCreateRequest, AnalysisRecalculateRequest
from app.schemas.property import NeighborhoodPayload, PropertyPayload
from app.services.analysis_service import AnalysisService


async def main():
    async with SessionLocal() as session:
        service = AnalysisService(session)
        analysis = await service.create_analysis(
            AnalysisCreateRequest(
                property=PropertyPayload(
                    propertyName="Crescent Bay Residences",
                    address="1000 Market Street",
                    city="Austin",
                    state="Texas",
                    zipCode="78701",
                    propertyType="Apartment",
                    bedrooms=2,
                    bathrooms=2,
                    areaSqft=1180,
                    yearBuilt=2020,
                    furnishingStatus="Semi Furnished",
                    floorNumber=5,
                    parkingAvailability="Covered",
                    parkingSpaces=1,
                    hasGym=True,
                    hasPool=True,
                    petFriendly=True,
                    gatedCommunity=True,
                    nearbyMetroDistance=0.7,
                    amenities=["Gym", "Pool", "Security"],
                ),
                neighborhood=NeighborhoodPayload(
                    schoolQualityScore=8,
                    floodRiskScore=3,
                    transitScore=7,
                    roadNoiseScore=4,
                    neighborhoodAppealScore=8,
                ),
                analyst_notes="Seeded demo analysis.",
            )
        )
        await service.recalculate_analysis(
            analysis.id,
            AnalysisRecalculateRequest(feedback_text="This property should be priced more premium"),
        )
        print(f"Seeded analysis {analysis.id}")


if __name__ == "__main__":
    asyncio.run(main())
