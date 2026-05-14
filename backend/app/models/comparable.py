import uuid

from sqlalchemy import ForeignKey, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class ComparableProperty(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "comparable_properties"

    recommendation_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("pricing_recommendations.id"), index=True, nullable=False
    )
    property_name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    monthly_rent: Mapped[float] = mapped_column(Float, nullable=False)
    bedrooms: Mapped[int] = mapped_column(Integer, nullable=False)
    bathrooms: Mapped[float] = mapped_column(Float, nullable=False)
    area_sqft: Mapped[int] = mapped_column(Integer, nullable=False)
    distance_miles: Mapped[float] = mapped_column(Float, nullable=False)
    similarity_score: Mapped[float] = mapped_column(Float, nullable=False)
    match_percentage: Mapped[float] = mapped_column(Float, nullable=False)
    selection_reason: Mapped[str] = mapped_column(Text, nullable=False)
    key_matching_factors_json: Mapped[str] = mapped_column(Text, default="[]", nullable=False)
    weight: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="active", nullable=False)

    recommendation = relationship("PricingRecommendation", back_populates="comparables")
    adjustments = relationship(
        "ComparableAdjustment", back_populates="comparable", cascade="all, delete-orphan"
    )


class ComparableAdjustment(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "comparable_adjustments"

    comparable_property_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("comparable_properties.id"), index=True, nullable=False
    )
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    reason: Mapped[str | None] = mapped_column(Text)
    previous_weight: Mapped[float] = mapped_column(Float, nullable=False)
    new_weight: Mapped[float] = mapped_column(Float, nullable=False)
    previous_status: Mapped[str] = mapped_column(String(50), nullable=False)
    new_status: Mapped[str] = mapped_column(String(50), nullable=False)

    comparable = relationship("ComparableProperty", back_populates="adjustments")
