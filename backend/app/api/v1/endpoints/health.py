"""Health check endpoint."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.config import Settings, get_settings
from app.schemas.health import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def get_health(settings: Annotated[Settings, Depends(get_settings)]) -> HealthResponse:
    """Return basic application and API status."""
    return HealthResponse(
        application_name=settings.app_name,
        status="ok",
        api_version=settings.api_version,
    )
