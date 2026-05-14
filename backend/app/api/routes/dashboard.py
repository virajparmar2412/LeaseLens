from fastapi import APIRouter

from app.schemas.dashboard import DashboardInsightsResponse
from app.services.dashboard_service import get_dashboard_insights

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/insights", response_model=DashboardInsightsResponse)
def dashboard_insights():
    return get_dashboard_insights()
