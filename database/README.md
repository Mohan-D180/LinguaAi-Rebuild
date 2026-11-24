# Database

The PostgreSQL schema is defined by SQLAlchemy models in [`../backend/app/models/`](../backend/app/models/), with versioned migrations in [`../backend/alembic/`](../backend/alembic/). The entity relationships and deletion rules are documented in [`../docs/database/erd.md`](../docs/database/erd.md).

Use Alembic as the source of truth for schema changes. This directory is reserved for database-wide operational documentation and non-sensitive development data; do not duplicate model definitions or migration scripts here.
