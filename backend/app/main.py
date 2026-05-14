from fastapi import FastAPI

from app.api.routes.analyses import router as analyses_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.health import router as health_router
from app.api.routes.pricing import router as pricing_router
from app.core.config import settings


def create_application() -> FastAPI:
    application = FastAPI(title=settings.app_name)
    application.include_router(health_router, prefix=settings.api_v1_prefix)
    application.include_router(pricing_router, prefix=settings.api_v1_prefix)
    application.include_router(dashboard_router, prefix=settings.api_v1_prefix)
    application.include_router(analyses_router, prefix=settings.api_v1_prefix)
    return application


app = create_application()
