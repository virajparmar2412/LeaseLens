import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class User(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(100), default="analyst", nullable=False)

    analyses = relationship("PropertyAnalysis", back_populates="user")
    feedback_messages = relationship("AnalystFeedback", back_populates="user")
    recommendation_events = relationship("RecommendationEvent", back_populates="user")
