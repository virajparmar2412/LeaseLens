"""initial schema"""

from alembic import op
import sqlalchemy as sa


revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=100), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_table(
        "properties",
        sa.Column("property_name", sa.String(length=255), nullable=False),
        sa.Column("address", sa.String(length=255), nullable=False),
        sa.Column("city", sa.String(length=120), nullable=False),
        sa.Column("state", sa.String(length=120), nullable=False),
        sa.Column("zip_code", sa.String(length=20), nullable=False),
        sa.Column("property_type", sa.String(length=80), nullable=False),
        sa.Column("bedrooms", sa.Integer(), nullable=False),
        sa.Column("bathrooms", sa.Float(), nullable=False),
        sa.Column("area_sqft", sa.Integer(), nullable=False),
        sa.Column("year_built", sa.Integer(), nullable=False),
        sa.Column("furnishing_status", sa.String(length=100), nullable=False),
        sa.Column("floor_number", sa.Integer(), nullable=False),
        sa.Column("parking_spaces", sa.Integer(), nullable=False),
        sa.Column("parking_availability", sa.String(length=100), nullable=False),
        sa.Column("has_gym", sa.Boolean(), nullable=False),
        sa.Column("has_pool", sa.Boolean(), nullable=False),
        sa.Column("pet_friendly", sa.Boolean(), nullable=False),
        sa.Column("gated_community", sa.Boolean(), nullable=False),
        sa.Column("nearby_metro_distance", sa.Float(), nullable=False),
        sa.Column("amenities_json", sa.String(length=1000), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_properties_city"), "properties", ["city"], unique=False)
    op.create_index(op.f("ix_properties_property_name"), "properties", ["property_name"], unique=False)
    op.create_index(op.f("ix_properties_property_type"), "properties", ["property_type"], unique=False)
    op.create_index(op.f("ix_properties_zip_code"), "properties", ["zip_code"], unique=False)
    op.create_table(
        "property_analyses",
        sa.Column("user_id", sa.Uuid(), nullable=True),
        sa.Column("property_id", sa.Uuid(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("analyst_notes", sa.Text(), nullable=True),
        sa.Column("latest_recommendation_id", sa.Uuid(), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["property_id"], ["properties.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_property_analyses_property_id"), "property_analyses", ["property_id"], unique=False)
    op.create_index(op.f("ix_property_analyses_user_id"), "property_analyses", ["user_id"], unique=False)
    op.create_table(
        "neighborhood_metrics",
        sa.Column("property_id", sa.Uuid(), nullable=False),
        sa.Column("school_quality_score", sa.Float(), nullable=False),
        sa.Column("flood_risk_score", sa.Float(), nullable=False),
        sa.Column("transit_score", sa.Float(), nullable=False),
        sa.Column("road_noise_score", sa.Float(), nullable=False),
        sa.Column("neighborhood_appeal_score", sa.Float(), nullable=False),
        sa.Column("crime_index", sa.Float(), nullable=False),
        sa.Column("walkability_score", sa.Float(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["property_id"], ["properties.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_neighborhood_metrics_property_id"), "neighborhood_metrics", ["property_id"], unique=False)
    op.create_table(
        "pricing_recommendations",
        sa.Column("analysis_id", sa.Uuid(), nullable=False),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("recommended_rent", sa.Float(), nullable=False),
        sa.Column("rent_low", sa.Float(), nullable=False),
        sa.Column("rent_high", sa.Float(), nullable=False),
        sa.Column("confidence_score", sa.Float(), nullable=False),
        sa.Column("price_per_sqft", sa.Float(), nullable=False),
        sa.Column("reasoning_summary", sa.Text(), nullable=False),
        sa.Column("market_trend_indicator", sa.String(length=500), nullable=False),
        sa.Column("pricing_factors_json", sa.Text(), nullable=False),
        sa.Column("neighborhood_summary_json", sa.Text(), nullable=False),
        sa.Column("adjustment_factors_json", sa.Text(), nullable=False),
        sa.Column("triggered_by", sa.String(length=100), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["analysis_id"], ["property_analyses.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_pricing_recommendations_analysis_id"), "pricing_recommendations", ["analysis_id"], unique=False)
    op.create_foreign_key(
        "fk_property_analyses_latest_recommendation",
        "property_analyses",
        "pricing_recommendations",
        ["latest_recommendation_id"],
        ["id"],
    )
    op.create_table(
        "analyst_feedback",
        sa.Column("analysis_id", sa.Uuid(), nullable=False),
        sa.Column("recommendation_id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=True),
        sa.Column("role", sa.String(length=50), nullable=False),
        sa.Column("message_text", sa.Text(), nullable=False),
        sa.Column("parsed_intent", sa.String(length=255), nullable=False),
        sa.Column("pricing_adjustment", sa.Float(), nullable=False),
        sa.Column("affected_recommendation_version", sa.Integer(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["analysis_id"], ["property_analyses.id"]),
        sa.ForeignKeyConstraint(["recommendation_id"], ["pricing_recommendations.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_analyst_feedback_analysis_id"), "analyst_feedback", ["analysis_id"], unique=False)
    op.create_index(op.f("ix_analyst_feedback_recommendation_id"), "analyst_feedback", ["recommendation_id"], unique=False)
    op.create_index(op.f("ix_analyst_feedback_user_id"), "analyst_feedback", ["user_id"], unique=False)
    op.create_table(
        "comparable_properties",
        sa.Column("recommendation_id", sa.Uuid(), nullable=False),
        sa.Column("property_name", sa.String(length=255), nullable=False),
        sa.Column("address", sa.String(length=255), nullable=False),
        sa.Column("monthly_rent", sa.Float(), nullable=False),
        sa.Column("bedrooms", sa.Integer(), nullable=False),
        sa.Column("bathrooms", sa.Float(), nullable=False),
        sa.Column("area_sqft", sa.Integer(), nullable=False),
        sa.Column("distance_miles", sa.Float(), nullable=False),
        sa.Column("similarity_score", sa.Float(), nullable=False),
        sa.Column("match_percentage", sa.Float(), nullable=False),
        sa.Column("selection_reason", sa.Text(), nullable=False),
        sa.Column("key_matching_factors_json", sa.Text(), nullable=False),
        sa.Column("weight", sa.Float(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["recommendation_id"], ["pricing_recommendations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_comparable_properties_recommendation_id"), "comparable_properties", ["recommendation_id"], unique=False)
    op.create_table(
        "recommendation_events",
        sa.Column("analysis_id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=True),
        sa.Column("event_type", sa.String(length=100), nullable=False),
        sa.Column("event_summary", sa.Text(), nullable=False),
        sa.Column("metadata_json", sa.Text(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["analysis_id"], ["property_analyses.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_recommendation_events_analysis_id"), "recommendation_events", ["analysis_id"], unique=False)
    op.create_index(op.f("ix_recommendation_events_user_id"), "recommendation_events", ["user_id"], unique=False)
    op.create_table(
        "recommendation_history",
        sa.Column("analysis_id", sa.Uuid(), nullable=False),
        sa.Column("recommendation_id", sa.Uuid(), nullable=False),
        sa.Column("previous_recommendation_value", sa.Float(), nullable=False),
        sa.Column("new_recommendation_value", sa.Float(), nullable=False),
        sa.Column("previous_confidence_score", sa.Float(), nullable=False),
        sa.Column("new_confidence_score", sa.Float(), nullable=False),
        sa.Column("change_reason", sa.Text(), nullable=False),
        sa.Column("trigger_type", sa.String(length=100), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["analysis_id"], ["property_analyses.id"]),
        sa.ForeignKeyConstraint(["recommendation_id"], ["pricing_recommendations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_recommendation_history_analysis_id"), "recommendation_history", ["analysis_id"], unique=False)
    op.create_index(op.f("ix_recommendation_history_recommendation_id"), "recommendation_history", ["recommendation_id"], unique=False)
    op.create_table(
        "comparable_adjustments",
        sa.Column("comparable_property_id", sa.Uuid(), nullable=False),
        sa.Column("action", sa.String(length=100), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("previous_weight", sa.Float(), nullable=False),
        sa.Column("new_weight", sa.Float(), nullable=False),
        sa.Column("previous_status", sa.String(length=50), nullable=False),
        sa.Column("new_status", sa.String(length=50), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["comparable_property_id"], ["comparable_properties.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_comparable_adjustments_comparable_property_id"), "comparable_adjustments", ["comparable_property_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_comparable_adjustments_comparable_property_id"), table_name="comparable_adjustments")
    op.drop_table("comparable_adjustments")
    op.drop_index(op.f("ix_recommendation_history_recommendation_id"), table_name="recommendation_history")
    op.drop_index(op.f("ix_recommendation_history_analysis_id"), table_name="recommendation_history")
    op.drop_table("recommendation_history")
    op.drop_index(op.f("ix_recommendation_events_user_id"), table_name="recommendation_events")
    op.drop_index(op.f("ix_recommendation_events_analysis_id"), table_name="recommendation_events")
    op.drop_table("recommendation_events")
    op.drop_index(op.f("ix_comparable_properties_recommendation_id"), table_name="comparable_properties")
    op.drop_table("comparable_properties")
    op.drop_index(op.f("ix_analyst_feedback_user_id"), table_name="analyst_feedback")
    op.drop_index(op.f("ix_analyst_feedback_recommendation_id"), table_name="analyst_feedback")
    op.drop_index(op.f("ix_analyst_feedback_analysis_id"), table_name="analyst_feedback")
    op.drop_table("analyst_feedback")
    op.drop_constraint("fk_property_analyses_latest_recommendation", "property_analyses", type_="foreignkey")
    op.drop_index(op.f("ix_pricing_recommendations_analysis_id"), table_name="pricing_recommendations")
    op.drop_table("pricing_recommendations")
    op.drop_index(op.f("ix_neighborhood_metrics_property_id"), table_name="neighborhood_metrics")
    op.drop_table("neighborhood_metrics")
    op.drop_index(op.f("ix_property_analyses_user_id"), table_name="property_analyses")
    op.drop_index(op.f("ix_property_analyses_property_id"), table_name="property_analyses")
    op.drop_table("property_analyses")
    op.drop_index(op.f("ix_properties_zip_code"), table_name="properties")
    op.drop_index(op.f("ix_properties_property_type"), table_name="properties")
    op.drop_index(op.f("ix_properties_property_name"), table_name="properties")
    op.drop_index(op.f("ix_properties_city"), table_name="properties")
    op.drop_table("properties")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
