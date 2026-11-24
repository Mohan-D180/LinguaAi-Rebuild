# LinguaAi PostgreSQL schema

This ERD describes the initial schema in `backend/app/models/` and its Alembic migration. It deliberately contains no business-specific tables beyond the requested learning entities.

```mermaid
erDiagram
    USERS ||--o| LEARNING_PROFILES : has
    USERS ||--o| USER_SETTINGS : configures
    USERS ||--o{ SESSIONS : starts
    USERS ||--o{ LEARNING_PROGRESS : accumulates
    USERS ||--o{ REFRESH_TOKENS : owns
    USERS ||--o{ AUDIO_ASSETS : owns

    LANGUAGES o|--o{ LEARNING_PROFILES : native_language
    LANGUAGES o|--o{ LEARNING_PROFILES : learning_language
    LANGUAGES ||--o{ SESSIONS : practiced_in
    LANGUAGES ||--o{ LEARNING_PROGRESS : measured_for

    SESSIONS ||--o{ MESSAGES : contains
    SESSIONS ||--o{ SESSION_ANALYSES : analyzed_by
    SESSIONS o|--o{ AUDIO_ASSETS : has_audio
    MESSAGES o|--o{ GRAMMAR_ERRORS : references
    MESSAGES o|--o{ VOCABULARY_FEEDBACK : references
    MESSAGES o|--o{ AUDIO_ASSETS : has_audio
    SESSION_ANALYSES ||--o{ GRAMMAR_ERRORS : identifies
    SESSION_ANALYSES ||--o{ VOCABULARY_FEEDBACK : identifies

    USERS {
        uuid id PK
        varchar email UK
        varchar password_hash
        varchar display_name
        boolean is_active
        timestamptz created_at
        timestamptz updated_at
    }

    LEARNING_PROFILES {
        uuid id PK
        uuid user_id FK,UK
        uuid native_language_id FK
        uuid learning_language_id FK
        varchar proficiency_level
        jsonb goals
        timestamptz created_at
        timestamptz updated_at
    }

    USER_SETTINGS {
        uuid id PK
        uuid user_id FK,UK
        varchar theme
        varchar timezone
        jsonb preferences
        timestamptz created_at
        timestamptz updated_at
    }

    LANGUAGES {
        uuid id PK
        varchar code UK
        varchar name
        varchar native_name
        boolean is_active
        timestamptz created_at
        timestamptz updated_at
    }

    SESSIONS {
        uuid id PK
        uuid user_id FK
        uuid language_id FK
        varchar title
        varchar status
        timestamptz started_at
        timestamptz ended_at
        jsonb context
        timestamptz created_at
        timestamptz updated_at
    }

    MESSAGES {
        uuid id PK
        uuid session_id FK
        integer sequence_number
        varchar role
        text content
        jsonb extra_data
        timestamptz created_at
        timestamptz updated_at
    }

    SESSION_ANALYSES {
        uuid id PK
        uuid session_id FK
        text summary
        jsonb results
        timestamptz created_at
        timestamptz updated_at
    }

    GRAMMAR_ERRORS {
        uuid id PK
        uuid analysis_id FK
        uuid message_id FK
        varchar category
        text original_text
        text suggested_text
        text explanation
        integer start_offset
        integer end_offset
        timestamptz created_at
        timestamptz updated_at
    }

    VOCABULARY_FEEDBACK {
        uuid id PK
        uuid analysis_id FK
        uuid message_id FK
        varchar term
        text definition
        text translation
        varchar status
        jsonb context
        timestamptz created_at
        timestamptz updated_at
    }

    LEARNING_PROGRESS {
        uuid id PK
        uuid user_id FK
        uuid language_id FK
        date progress_date
        integer minutes_practiced
        integer sessions_completed
        integer words_learned
        numeric accuracy_percent
        jsonb metrics
        timestamptz created_at
        timestamptz updated_at
    }

    REFRESH_TOKENS {
        uuid id PK
        uuid user_id FK
        varchar token_hash UK
        timestamptz expires_at
        timestamptz revoked_at
        timestamptz last_used_at
        timestamptz created_at
        timestamptz updated_at
    }

    AUDIO_ASSETS {
        uuid id PK
        uuid user_id FK
        uuid session_id FK
        uuid message_id FK
        varchar storage_key UK
        varchar mime_type
        bigint size_bytes
        integer duration_ms
        varchar checksum_sha256
        timestamptz created_at
        timestamptz updated_at
    }
```

## Relationship and deletion rules

- Each user can have zero or one learning profile and zero or one settings record. Deleting the user cascades to both.
- Users can have many sessions, progress records, refresh-token records, and audio-asset records. Deleting a user cascades to those records.
- A learning profile may reference a native language and a learning language. Those references are nullable and become `NULL` if a catalog language is deleted.
- Each session belongs to exactly one user and one language. Deleting a user cascades to their sessions; deleting a referenced language is restricted.
- A session contains zero or many ordered messages and zero or many analysis runs. Deleting a session cascades to its messages, analyses, and linked audio metadata.
- An analysis belongs to one session and may identify many grammar errors and vocabulary feedback entries. Deleting the analysis cascades to those findings.
- A finding may reference zero or one message. Deleting a message preserves the finding but clears its message reference.
- Each daily progress record belongs to one user and one language. The `(user_id, language_id, progress_date)` combination is unique; language deletion is restricted while progress refers to it.
- Refresh-token records store a unique token hash, never the raw token. They belong to one user and are deleted with that user.
- Audio assets belong to one user and may be linked to a session or message. PostgreSQL stores metadata and an external `storage_key`, not audio binary data.

Unique constraints protect user email, language code, the one-to-one profile/settings user references, per-session message order, refresh-token hashes, audio storage keys, and daily progress aggregates. Foreign keys and commonly filtered parent/date fields are indexed.
