import uuid

from sqlalchemy import ForeignKey, Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class RecommendationHistory(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "recommendation_history"

    analysis_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("property_analyses.id"), index=True, nullable=False
    )
    recommendation_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("pricing_recommendations.id"), index=True, nullable=False
    )
    previous_recommendation_value: Mapped[float] = mapped_column(Float, nullable=False)
    new_recommendation_value: Mapped[float] = mapped_column(Float, nullable=False)
    previous_confidence_score: Mapped[float] = mapped_column(Float, nullable=False)
    new_confidence_score: Mapped[float] = mapped_column(Float, nullable=False)
    change_reason: Mapped[str] = mapped_column(Text, nullable=False)
    trigger_type: Mapped[str] = mapped_column(String(100), nullable=False)

    recommendation = relationship("PricingRecommendation", back_populates="history_entries")


class RecommendationEvent(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "recommendation_events"

    analysis_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("property_analyses.id"), index=True, nullable=False
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), index=True)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    event_summary: Mapped[str] = mapped_column(Text, nullable=False)
    metadata_json: Mapped[str] = mapped_column(Text, default="{}", nullable=False)

    analysis = relationship("PropertyAnalysis", back_populates="events")
    user = relationship("User", back_populates="recommendation_events")
