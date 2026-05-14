from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Property(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "properties"

    property_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(120), index=True, nullable=False)
    state: Mapped[str] = mapped_column(String(120), nullable=False)
    zip_code: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    property_type: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    bedrooms: Mapped[int] = mapped_column(Integer, nullable=False)
    bathrooms: Mapped[float] = mapped_column(Float, nullable=False)
    area_sqft: Mapped[int] = mapped_column(Integer, nullable=False)
    year_built: Mapped[int] = mapped_column(Integer, nullable=False)
    furnishing_status: Mapped[str] = mapped_column(String(100), nullable=False)
    floor_number: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    parking_spaces: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    parking_availability: Mapped[str] = mapped_column(String(100), nullable=False)
    has_gym: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_pool: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    pet_friendly: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    gated_community: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    nearby_metro_distance: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    amenities_json: Mapped[str] = mapped_column(String(1000), default="[]", nullable=False)
    latitude: Mapped[float | None] = mapped_column(Float)
    longitude: Mapped[float | None] = mapped_column(Float)

    analyses = relationship("PropertyAnalysis", back_populates="property")
    neighborhood_metrics = relationship(
        "NeighborhoodMetric", back_populates="property", cascade="all, delete-orphan"
    )
