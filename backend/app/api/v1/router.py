"""Version 1 API router."""

from fastapi import APIRouter

from app.api.v1.endpoints import database_health, health

api_router = APIRouter(prefix="/v1")
api_router.include_router(health.router, tags=["health"])
api_router.include_router(database_health.router, tags=["health"])
