from app.schemas.dashboard import DashboardInsightsResponse


def get_dashboard_insights() -> DashboardInsightsResponse:
    return DashboardInsightsResponse(
        metrics=[
            {"label": "Active Pricing Runs", "value": "128", "delta": "+12.4%"},
            {"label": "Avg. Confidence", "value": "84%", "delta": "+4.1%"},
            {"label": "Override Rate", "value": "17%", "delta": "-2.8%"},
            {"label": "Comp Match Health", "value": "91%", "delta": "+3.3%"},
        ],
        recommendation_volume=[
            {"month": "Jan", "count": 44},
            {"month": "Feb", "count": 58},
            {"month": "Mar", "count": 61},
            {"month": "Apr", "count": 76},
        ],
        confidence_distribution=[
            {"bucket": "70-79%", "count": 21},
            {"bucket": "80-89%", "count": 49},
            {"bucket": "90%+", "count": 33},
        ],
    )
