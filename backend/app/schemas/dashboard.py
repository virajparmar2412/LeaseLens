from pydantic import BaseModel


class DashboardMetric(BaseModel):
    label: str
    value: str
    delta: str


class DashboardInsightsResponse(BaseModel):
    metrics: list[DashboardMetric]
    recommendation_volume: list[dict]
    confidence_distribution: list[dict]
