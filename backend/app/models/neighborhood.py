import uuid

from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class NeighborhoodMetric(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "neighborhood_metrics"

    property_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("properties.id"), index=True, nullable=False
    )
    school_quality_score: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    flood_risk_score: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    transit_score: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    road_noise_score: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    neighborhood_appeal_score: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    crime_index: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    walkability_score: Mapped[float] = mapped_column(Float, default=0, nullable=False)

    property = relationship("Property", back_populates="neighborhood_metrics")
