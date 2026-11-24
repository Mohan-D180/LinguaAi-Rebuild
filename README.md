# LinguaAi

LinguaAi is a foundation for a full-stack language application. The planned stack is React, TypeScript, and Vite for the frontend; Python and FastAPI for the backend; PostgreSQL for persistent data; and separate AI services for speech recognition, a locally hosted language model, and text-to-speech.

> **Project status:** The frontend and backend are initialized with development placeholders and a basic health API. Database migrations, authentication, AI services, and production deployment workflows have not been added yet.

## Repository structure

| Directory | Purpose |
| --- | --- |
| [`frontend/`](frontend/README.md) | Browser application, planned with React, TypeScript, and Vite. |
| [`backend/`](backend/README.md) | HTTP API and application logic, planned with Python and FastAPI. |
| [`ai-services/`](ai-services/README.md) | Isolated speech recognition, local LLM, and text-to-speech components. |
| [`infrastructure/`](infrastructure/README.md) | Docker Compose development environment and future deployment infrastructure. |
| [`database/`](database/README.md) | PostgreSQL schema, migrations, and safe development seed data. |
| [`tests/`](tests/README.md) | Shared testing guidance and, as the project grows, cross-component test support. |
| [`docs/`](docs/README.md) | Architecture notes, decisions, and developer/operator documentation. |
| [`.github/workflows/`](.github/workflows/README.md) | GitHub Actions automation, to be added when there are checks and build targets to run. |

## Getting started

### Prerequisites

To run both application services with Docker, install:

- Docker Engine or Docker Desktop with the Compose plugin

From the repository root:

```powershell
Copy-Item .env.example .env
docker compose up --build
```

Open `http://localhost:5173`. The frontend development server proxies `/api` requests to the backend over the private Compose network. See [`infrastructure/README.md`](infrastructure/README.md) for health checks, logs, configuration, and shutdown commands.

To run a service directly without Docker, follow the instructions in [`frontend/README.md`](frontend/README.md) or [`backend/README.md`](backend/README.md).

AI model runtimes and model files will be documented when the AI services are implemented. Model files and other large/generated assets should not be committed.

## Development principles

- Keep frontend, backend, and AI service responsibilities clearly separated.
- Treat PostgreSQL migrations as the source of truth for schema changes.
- Keep secrets, local environment files, model weights, and generated outputs out of version control and container images.
- Add automated checks when their respective build and test commands exist.
