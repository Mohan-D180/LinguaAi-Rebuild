"""Health endpoint response schema."""

from typing import Literal

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Public health status returned by the API."""

    application_name: str
    status: Literal["ok"]
    api_version: str


class DatabaseHealthResponse(BaseModel):
    """Public database connectivity status."""

    status: Literal["ok"]
    database: Literal["connected"]
