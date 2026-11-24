# LinguaAi backend

A modular FastAPI service, served as an ASGI application by Uvicorn. This initial scaffold provides a versioned health endpoint, environment-based settings, CORS configuration, JSON logs, and a pytest test suite. It does not connect to PostgreSQL or implement authentication.

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

Copy `.env.example` to `.env` to customize local settings. The defaults work for local development.

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

## Test and lint

```bash
pytest
ruff check .
ruff format --check .
```

## Project structure

- `app/core/` contains settings and structured logging.
- `app/api/v1/` contains versioned API routers and endpoints.
- `app/schemas/` contains validated request and response models.
- `tests/` contains pytest tests for API behavior.
- `main.py` exposes the ASGI application for Uvicorn.

Configuration is loaded from environment variables, with an optional local `.env` file. `CORS_ORIGINS` is a comma-separated list of allowed origins. Keep local `.env` files and secrets out of version control.
