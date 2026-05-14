import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class PropertyAnalysis(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "property_analyses"

    user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), index=True)
    property_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("properties.id"), index=True)
    status: Mapped[str] = mapped_column(String(50), default="active", nullable=False)
    analyst_notes: Mapped[str | None] = mapped_column(Text)
    latest_recommendation_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("pricing_recommendations.id")
    )

    user = relationship("User", back_populates="analyses")
    property = relationship("Property", back_populates="analyses")
    recommendations = relationship(
        "PricingRecommendation",
        back_populates="analysis",
        cascade="all, delete-orphan",
        foreign_keys="PricingRecommendation.analysis_id",
    )
    feedback_messages = relationship(
        "AnalystFeedback", back_populates="analysis", cascade="all, delete-orphan"
    )
    events = relationship(
        "RecommendationEvent", back_populates="analysis", cascade="all, delete-orphan"
    )
