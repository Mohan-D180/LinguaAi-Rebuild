"""User accounts, learning profiles, and per-user settings."""

from typing import TYPE_CHECKING, Any
from uuid import UUID

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import text

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.language import Language
    from app.models.learning_progress import LearningProgress
    from app.models.learning_session import AudioAsset, LearningSession
    from app.models.refresh_token import RefreshToken


class User(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Application user account."""

    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("email", name="uq_users_email"),
        Index("ix_users_created_at", "created_at"),
    )

    email: Mapped[str] = mapped_column(String(320), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    display_name: Mapped[str | None] = mapped_column(String(120))
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("true"),
    )

    learning_profile: Mapped["LearningProfile | None"] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
    )
    settings: Mapped["UserSettings | None"] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
    )
    sessions: Mapped[list["LearningSession"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    progress_records: Mapped[list["LearningProgress"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    audio_assets: Mapped[list["AudioAsset"]] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan",
    )


class LearningProfile(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """A user's learning goals, proficiency, and language preferences."""

    __tablename__ = "learning_profiles"
    __table_args__ = (
        UniqueConstraint("user_id", name="uq_learning_profiles_user_id"),
        CheckConstraint(
            "proficiency_level IS NULL OR proficiency_level IN "
            "('A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'native')",
            name="ck_learning_profiles_proficiency_level",
        ),
        Index("ix_learning_profiles_native_language_id", "native_language_id"),
        Index("ix_learning_profiles_learning_language_id", "learning_language_id"),
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    native_language_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("languages.id", ondelete="SET NULL"),
    )
    learning_language_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("languages.id", ondelete="SET NULL"),
    )
    proficiency_level: Mapped[str | None] = mapped_column(String(16))
    goals: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        server_default=text("'{}'::jsonb"),
    )

    user: Mapped["User"] = relationship(back_populates="learning_profile")
    native_language: Mapped["Language | None"] = relationship(
        back_populates="native_profiles",
        foreign_keys=[native_language_id],
    )
    learning_language: Mapped["Language | None"] = relationship(
        back_populates="learning_profiles",
        foreign_keys=[learning_language_id],
    )


class UserSettings(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """A user's interface and notification preferences."""

    __tablename__ = "user_settings"
    __table_args__ = (
        UniqueConstraint("user_id", name="uq_user_settings_user_id"),
        CheckConstraint("theme IN ('system', 'light', 'dark')", name="ck_user_settings_theme"),
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    theme: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        default="system",
        server_default="system",
    )
    timezone: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        default="UTC",
        server_default="UTC",
    )
    preferences: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        server_default=text("'{}'::jsonb"),
    )

    user: Mapped["User"] = relationship(back_populates="settings")
