import uuid

from sqlalchemy import ForeignKey, Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class PricingRecommendation(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "pricing_recommendations"

    analysis_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("property_analyses.id"), index=True, nullable=False
    )
    version_number: Mapped[int] = mapped_column(default=1, nullable=False)
    recommended_rent: Mapped[float] = mapped_column(Float, nullable=False)
    rent_low: Mapped[float] = mapped_column(Float, nullable=False)
    rent_high: Mapped[float] = mapped_column(Float, nullable=False)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False)
    price_per_sqft: Mapped[float] = mapped_column(Float, nullable=False)
    reasoning_summary: Mapped[str] = mapped_column(Text, nullable=False)
    market_trend_indicator: Mapped[str] = mapped_column(String(500), nullable=False)
    pricing_factors_json: Mapped[str] = mapped_column(Text, default="[]", nullable=False)
    neighborhood_summary_json: Mapped[str] = mapped_column(Text, default="[]", nullable=False)
    adjustment_factors_json: Mapped[str] = mapped_column(Text, default="{}", nullable=False)
    triggered_by: Mapped[str] = mapped_column(String(100), default="initial_generation", nullable=False)

    analysis = relationship(
        "PropertyAnalysis",
        back_populates="recommendations",
        foreign_keys=[analysis_id],
    )
    comparables = relationship(
        "ComparableProperty", back_populates="recommendation", cascade="all, delete-orphan"
    )
    feedback_messages = relationship("AnalystFeedback", back_populates="recommendation")
    history_entries = relationship(
        "RecommendationHistory", back_populates="recommendation", cascade="all, delete-orphan"
    )
