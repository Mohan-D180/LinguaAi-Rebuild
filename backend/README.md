# LinguaAi backend

A modular FastAPI service, served as an ASGI application by Uvicorn. It uses SQLAlchemy 2.x and Psycopg to connect to PostgreSQL, with Alembic for schema migrations. The initial core learning schema is defined, but authentication flows and business logic are not implemented.

## Requirements

- Python 3.11 or newer

## Set up a virtual environment

Run these commands from the `backend/` directory.

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Copy `.env.example` to `.env` and set `DATABASE_URL` to a reachable PostgreSQL instance. The example uses a local PostgreSQL service and development-only placeholder credentials; replace them for your environment. For Docker Compose, configure the root `.env` file as described in [`../infrastructure/README.md`](../infrastructure/README.md).

## Run the API

```bash
uvicorn main:app --reload
```

The service listens on `http://127.0.0.1:8000` by default. Interactive API documentation is available at `/docs`, with the OpenAPI schema at `/openapi.json`.

### Health check

```text
GET /api/v1/health
```

Example response:

```json
{
  "application_name": "LinguaAi",
  "status": "ok",
  "api_version": "v1"
}
```

Database readiness is checked separately:

```text
GET /api/v1/health/database
```

The database health endpoint executes `SELECT 1` and returns HTTP 503 if PostgreSQL is unavailable.

## Test and lint

```bash
pytest
ruff check .
ruff format --check .
```

The database connectivity test requires a reachable PostgreSQL instance configured by `DATABASE_URL`. With Docker Compose running, run it using `docker compose exec backend pytest`.

## Database migrations

Alembic is configured in `alembic.ini` and `alembic/`. Apply available migrations with:

```bash
alembic upgrade head
```

The initial revision creates the core user, language, session, analysis, feedback, progress, token, and audio-metadata tables. Future model modules must be imported by `app/models/__init__.py` before generating autogenerate revisions.

## Database concepts

- **Connection pooling:** SQLAlchemy reuses open PostgreSQL connections instead of creating a new connection for every request. `pool_pre_ping=True` checks a pooled connection before reuse.
- **ORM:** SQLAlchemy maps Python model classes to database tables; `app/db/base.py` provides the declarative base for future models.
- **Migrations:** Alembic records and applies ordered schema changes so database structure can evolve consistently across environments.
- **Sessions:** A SQLAlchemy session is a short-lived unit of work. FastAPI's `get_db` dependency provides one session per request and closes it when the request finishes.

## Project structure

- `app/core/` contains settings and structured logging.
- `app/db/` contains the SQLAlchemy base and mixins, engine, session factory, and FastAPI session dependency.
- `app/models/` contains the twelve core learning-schema models registered with Alembic.
- `app/api/v1/` contains versioned API routers and endpoints.
- `alembic/` contains migration configuration and revision scripts.
- `app/schemas/` contains validated request and response models.
- `tests/` contains pytest tests for API behavior.
- `docs/database/erd.md` documents the entity relationships and deletion rules.
- `main.py` exposes the ASGI application for Uvicorn.

Configuration is loaded from environment variables, with an optional local `.env` file. `CORS_ORIGINS` is a comma-separated list of allowed origins. Keep local `.env` files and secrets out of version control.
