"""Integration checks for core ORM models and relationships."""

import hashlib
from datetime import UTC, date, datetime, timedelta
from uuid import uuid4

from sqlalchemy.orm import configure_mappers

from app.db.session import SessionLocal
from app.models import (
    AudioAsset,
    GrammarError,
    Language,
    LearningProfile,
    LearningProgress,
    LearningSession,
    Message,
    RefreshToken,
    SessionAnalysis,
    User,
    UserSettings,
    VocabularyFeedback,
)


def test_core_models_flush_with_relationships() -> None:
    configure_mappers()
    suffix = uuid4().hex
    language = Language(
        code=f"en-{suffix[:8]}",
        name="English",
        native_name="English",
    )
    user = User(email=f"{suffix}@example.test", password_hash="test-hash")
    profile = LearningProfile(
        user=user,
        native_language=language,
        learning_language=language,
        goals={"daily_minutes": 10},
    )
    settings = UserSettings(user=user)
    learning_session = LearningSession(user=user, language=language)
    message = Message(
        session=learning_session,
        sequence_number=1,
        role="user",
        content="I am learning English.",
    )
    analysis = SessionAnalysis(session=learning_session, results={"score": 90})
    grammar_error = GrammarError(
        analysis=analysis,
        message=message,
        category="tense",
        original_text="I learn yesterday.",
        suggested_text="I learned yesterday.",
        start_offset=2,
        end_offset=7,
    )
    vocabulary = VocabularyFeedback(
        analysis=analysis,
        message=message,
        term="practice",
        status="new",
    )
    progress = LearningProgress(
        user=user,
        language=language,
        progress_date=date.today(),
        minutes_practiced=10,
        sessions_completed=1,
        words_learned=2,
    )
    refresh_token = RefreshToken(
        user=user,
        token_hash=hashlib.sha256(suffix.encode()).hexdigest(),
        expires_at=datetime.now(UTC) + timedelta(days=1),
    )
    audio_asset = AudioAsset(
        owner=user,
        session=learning_session,
        message=message,
        storage_key=f"test/{suffix}.wav",
        mime_type="audio/wav",
        size_bytes=128,
    )

    session = SessionLocal()
    try:
        session.add_all(
            [
                user,
                language,
                profile,
                settings,
                learning_session,
                message,
                analysis,
                grammar_error,
                vocabulary,
                progress,
                refresh_token,
                audio_asset,
            ]
        )
        session.flush()

        assert profile.user is user
        assert settings.user is user
        assert learning_session.messages == [message]
        assert learning_session.analyses == [analysis]
        assert analysis.grammar_errors == [grammar_error]
        assert analysis.vocabulary_feedback == [vocabulary]
        assert audio_asset.owner is user
        assert audio_asset.message is message
    finally:
        session.rollback()
        session.close()
