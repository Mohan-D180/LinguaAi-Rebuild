"""Per-day learning progress aggregates."""

from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING, Any
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    Date,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.language import Language
    from app.models.user import User


class LearningProgress(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """A user's daily aggregate learning progress for one language."""

    __tablename__ = "learning_progress"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "language_id",
            "progress_date",
            name="uq_learning_progress_user_language_date",
        ),
        CheckConstraint("minutes_practiced >= 0", name="ck_learning_progress_minutes"),
        CheckConstraint("sessions_completed >= 0", name="ck_learning_progress_sessions"),
        CheckConstraint("words_learned >= 0", name="ck_learning_progress_words"),
        CheckConstraint(
            "accuracy_percent IS NULL OR (accuracy_percent >= 0 AND accuracy_percent <= 100)",
            name="ck_learning_progress_accuracy",
        ),
        Index("ix_learning_progress_user_date", "user_id", "progress_date"),
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    language_id: Mapped[UUID] = mapped_column(
        ForeignKey("languages.id", ondelete="RESTRICT"),
        nullable=False,
    )
    progress_date: Mapped[date] = mapped_column(Date, nullable=False)
    minutes_practiced: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )
    sessions_completed: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )
    words_learned: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )
    accuracy_percent: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))
    metrics: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        server_default=text("'{}'::jsonb"),
    )

    user: Mapped["User"] = relationship(back_populates="progress_records")
    language: Mapped["Language"] = relationship(back_populates="progress_records")
