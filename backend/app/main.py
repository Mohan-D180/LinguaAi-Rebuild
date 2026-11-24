"""FastAPI application factory and ASGI application."""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import Settings, get_settings
from app.core.logging_config import configure_logging

logger = logging.getLogger(__name__)


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create the API application with its runtime configuration."""
    app_settings = settings or get_settings()
    configure_logging(app_settings.log_level)

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        logger.info(
            "application_started",
            extra={
                "application_name": app_settings.app_name,
                "api_version": app_settings.api_version,
            },
        )
        yield
        logger.info("application_stopped", extra={"application_name": app_settings.app_name})

    application = FastAPI(
        title=app_settings.app_name,
        version=app_settings.api_version,
        description="Versioned API for the LinguaAi application.",
        lifespan=lifespan,
    )
    application.state.settings = app_settings
    application.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.allowed_origins,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(api_router, prefix="/api")

    if settings is not None:
        application.dependency_overrides[get_settings] = lambda: app_settings

    return application


app = create_app()
