import uuid

from sqlalchemy import ForeignKey, Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class AnalystFeedback(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "analyst_feedback"

    analysis_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("property_analyses.id"), index=True, nullable=False
    )
    recommendation_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("pricing_recommendations.id"), index=True, nullable=False
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), index=True)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    message_text: Mapped[str] = mapped_column(Text, nullable=False)
    parsed_intent: Mapped[str] = mapped_column(String(255), nullable=False)
    pricing_adjustment: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    affected_recommendation_version: Mapped[int] = mapped_column(nullable=False)

    analysis = relationship("PropertyAnalysis", back_populates="feedback_messages")
    recommendation = relationship("PricingRecommendation", back_populates="feedback_messages")
    user = relationship("User", back_populates="feedback_messages")
