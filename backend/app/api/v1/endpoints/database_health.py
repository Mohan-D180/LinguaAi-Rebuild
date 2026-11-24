"""PostgreSQL connectivity health endpoint."""

import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.health import DatabaseHealthResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/health/database", response_model=DatabaseHealthResponse)
def get_database_health(
    session: Annotated[Session, Depends(get_db)],
) -> DatabaseHealthResponse:
    """Return database connectivity status after executing a lightweight query."""
    try:
        session.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        logger.exception("database_health_check_failed")
        raise HTTPException(status_code=503, detail="Database unavailable") from exc

    return DatabaseHealthResponse(status="ok", database="connected")
