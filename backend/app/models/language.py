"""Supported language catalog."""

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Index, String, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.learning_progress import LearningProgress
    from app.models.learning_session import LearningSession
    from app.models.user import LearningProfile


class Language(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """A language available for learning."""

    __tablename__ = "languages"
    __table_args__ = (
        UniqueConstraint("code", name="uq_languages_code"),
        Index("ix_languages_is_active", "is_active"),
    )

    code: Mapped[str] = mapped_column(String(35), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    native_name: Mapped[str | None] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("true"),
    )

    sessions: Mapped[list["LearningSession"]] = relationship(back_populates="language")
    progress_records: Mapped[list["LearningProgress"]] = relationship(
        back_populates="language",
    )
    native_profiles: Mapped[list["LearningProfile"]] = relationship(
        foreign_keys="LearningProfile.native_language_id",
        back_populates="native_language",
    )
    learning_profiles: Mapped[list["LearningProfile"]] = relationship(
        foreign_keys="LearningProfile.learning_language_id",
        back_populates="learning_language",
    )
