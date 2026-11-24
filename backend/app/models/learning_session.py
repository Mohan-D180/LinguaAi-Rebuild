"""Learning sessions, messages, analyses, feedback, and audio metadata."""

from datetime import datetime
from typing import TYPE_CHECKING, Any
from uuid import UUID

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.language import Language
    from app.models.user import User


class LearningSession(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """A user's conversation or practice session in a language."""

    __tablename__ = "sessions"
    __table_args__ = (
        CheckConstraint(
            "status IN ('active', 'completed', 'abandoned')",
            name="ck_sessions_status",
        ),
        CheckConstraint(
            "ended_at IS NULL OR ended_at >= started_at",
            name="ck_sessions_ended_at",
        ),
        Index("ix_sessions_user_created_at", "user_id", "created_at"),
        Index("ix_sessions_language_id", "language_id"),
        Index("ix_sessions_status", "status"),
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    language_id: Mapped[UUID] = mapped_column(
        ForeignKey("languages.id", ondelete="RESTRICT"),
        nullable=False,
    )
    title: Mapped[str | None] = mapped_column(String(200))
    status: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        default="active",
        server_default="active",
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    context: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        server_default=text("'{}'::jsonb"),
    )

    user: Mapped["User"] = relationship(back_populates="sessions")
    language: Mapped["Language"] = relationship(back_populates="sessions")
    messages: Mapped[list["Message"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="Message.sequence_number",
    )
    analyses: Mapped[list["SessionAnalysis"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
    )
    audio_assets: Mapped[list["AudioAsset"]] = relationship(
        back_populates="session",
        cascade="all, delete",
        passive_deletes=True,
    )


class Message(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """An ordered user, assistant, or system message within a session."""

    __tablename__ = "messages"
    __table_args__ = (
        UniqueConstraint(
            "session_id",
            "sequence_number",
            name="uq_messages_session_sequence",
        ),
        CheckConstraint(
            "role IN ('user', 'assistant', 'system')",
            name="ck_messages_role",
        ),
        CheckConstraint("sequence_number >= 1", name="ck_messages_sequence_number"),
        CheckConstraint("length(content) > 0", name="ck_messages_content"),
        Index("ix_messages_session_created_at", "session_id", "created_at"),
    )

    session_id: Mapped[UUID] = mapped_column(
        ForeignKey("sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    sequence_number: Mapped[int] = mapped_column(Integer, nullable=False)
    role: Mapped[str] = mapped_column(String(16), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    extra_data: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        server_default=text("'{}'::jsonb"),
    )

    session: Mapped["LearningSession"] = relationship(back_populates="messages")
    grammar_errors: Mapped[list["GrammarError"]] = relationship(back_populates="message")
    vocabulary_feedback: Mapped[list["VocabularyFeedback"]] = relationship(
        back_populates="message",
    )
    audio_assets: Mapped[list["AudioAsset"]] = relationship(back_populates="message")


class SessionAnalysis(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """An analysis run over a learning session."""

    __tablename__ = "session_analyses"
    __table_args__ = (Index("ix_session_analyses_session_created_at", "session_id", "created_at"),)

    session_id: Mapped[UUID] = mapped_column(
        ForeignKey("sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    summary: Mapped[str | None] = mapped_column(Text)
    results: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        server_default=text("'{}'::jsonb"),
    )

    session: Mapped["LearningSession"] = relationship(back_populates="analyses")
    grammar_errors: Mapped[list["GrammarError"]] = relationship(
        back_populates="analysis",
        cascade="all, delete-orphan",
    )
    vocabulary_feedback: Mapped[list["VocabularyFeedback"]] = relationship(
        back_populates="analysis",
        cascade="all, delete-orphan",
    )


class GrammarError(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """A grammar issue identified by a session analysis."""

    __tablename__ = "grammar_errors"
    __table_args__ = (
        CheckConstraint(
            "start_offset IS NULL OR start_offset >= 0",
            name="ck_grammar_errors_start_offset",
        ),
        CheckConstraint(
            "end_offset IS NULL OR end_offset >= 0",
            name="ck_grammar_errors_end_offset",
        ),
        CheckConstraint(
            "start_offset IS NULL OR end_offset IS NULL OR end_offset >= start_offset",
            name="ck_grammar_errors_offset_order",
        ),
        Index("ix_grammar_errors_analysis_category", "analysis_id", "category"),
        Index("ix_grammar_errors_message_id", "message_id"),
    )

    analysis_id: Mapped[UUID] = mapped_column(
        ForeignKey("session_analyses.id", ondelete="CASCADE"),
        nullable=False,
    )
    message_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("messages.id", ondelete="SET NULL"),
    )
    category: Mapped[str] = mapped_column(String(64), nullable=False)
    original_text: Mapped[str] = mapped_column(Text, nullable=False)
    suggested_text: Mapped[str | None] = mapped_column(Text)
    explanation: Mapped[str | None] = mapped_column(Text)
    start_offset: Mapped[int | None] = mapped_column(Integer)
    end_offset: Mapped[int | None] = mapped_column(Integer)

    analysis: Mapped["SessionAnalysis"] = relationship(back_populates="grammar_errors")
    message: Mapped["Message | None"] = relationship(back_populates="grammar_errors")


class VocabularyFeedback(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Vocabulary guidance identified by a session analysis."""

    __tablename__ = "vocabulary_feedback"
    __table_args__ = (
        CheckConstraint(
            "status IN ('new', 'learning', 'known')",
            name="ck_vocabulary_feedback_status",
        ),
        CheckConstraint("length(trim(term)) > 0", name="ck_vocabulary_feedback_term"),
        Index("ix_vocabulary_feedback_analysis_term", "analysis_id", "term"),
        Index("ix_vocabulary_feedback_message_id", "message_id"),
    )

    analysis_id: Mapped[UUID] = mapped_column(
        ForeignKey("session_analyses.id", ondelete="CASCADE"),
        nullable=False,
    )
    message_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("messages.id", ondelete="SET NULL"),
    )
    term: Mapped[str] = mapped_column(String(200), nullable=False)
    definition: Mapped[str | None] = mapped_column(Text)
    translation: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        default="new",
        server_default="new",
    )
    context: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
        server_default=text("'{}'::jsonb"),
    )

    analysis: Mapped["SessionAnalysis"] = relationship(back_populates="vocabulary_feedback")
    message: Mapped["Message | None"] = relationship(back_populates="vocabulary_feedback")


class AudioAsset(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Metadata for audio stored outside PostgreSQL."""

    __tablename__ = "audio_assets"
    __table_args__ = (
        UniqueConstraint("storage_key", name="uq_audio_assets_storage_key"),
        CheckConstraint("size_bytes > 0", name="ck_audio_assets_size_bytes"),
        CheckConstraint(
            "duration_ms IS NULL OR duration_ms >= 0",
            name="ck_audio_assets_duration_ms",
        ),
        CheckConstraint(
            "checksum_sha256 IS NULL OR length(checksum_sha256) = 64",
            name="ck_audio_assets_checksum_sha256",
        ),
        Index("ix_audio_assets_user_created_at", "user_id", "created_at"),
        Index("ix_audio_assets_session_id", "session_id"),
        Index("ix_audio_assets_message_id", "message_id"),
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    session_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("sessions.id", ondelete="CASCADE"),
    )
    message_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("messages.id", ondelete="SET NULL"),
    )
    storage_key: Mapped[str] = mapped_column(String(1024), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(127), nullable=False)
    size_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False)
    duration_ms: Mapped[int | None] = mapped_column(Integer)
    checksum_sha256: Mapped[str | None] = mapped_column(String(64))

    owner: Mapped["User"] = relationship(back_populates="audio_assets")
    session: Mapped["LearningSession | None"] = relationship(back_populates="audio_assets")
    message: Mapped["Message | None"] = relationship(back_populates="audio_assets")
