from fastapi import FastAPI

from app.api.routes.advisor import router as advisor_router
from app.api.routes.health import router as health_router
from app.core.config import get_settings
from app.core.logging import configure_logging

configure_logging()
settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="A deployable Multi-Agent smart financial advisor demo.",
)

app.include_router(health_router)
app.include_router(advisor_router, prefix=settings.api_prefix)
