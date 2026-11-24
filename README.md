# LinguaAi

LinguaAi is a foundation for a full-stack language application. The planned stack is React, TypeScript, and Vite for the frontend; Python and FastAPI for the backend; PostgreSQL for persistent data; and separate AI services for speech recognition, a locally hosted language model, and text-to-speech.

> **Project status:** This repository currently contains structure and documentation only. Application code, dependency manifests, database migrations, and deployment workflows have not been added yet.

## Repository structure

| Directory | Purpose |
| --- | --- |
| [`frontend/`](frontend/README.md) | Browser application, planned with React, TypeScript, and Vite. |
| [`backend/`](backend/README.md) | HTTP API and application logic, planned with Python and FastAPI. |
| [`ai-services/`](ai-services/README.md) | Isolated speech recognition, local LLM, and text-to-speech components. |
| [`infrastructure/`](infrastructure/README.md) | Local development and deployment infrastructure, including future container configuration. |
| [`database/`](database/README.md) | PostgreSQL schema, migrations, and safe development seed data. |
| [`tests/`](tests/README.md) | Shared testing guidance and, as the project grows, cross-component test support. |
| [`docs/`](docs/README.md) | Architecture notes, decisions, and developer/operator documentation. |
| [`.github/workflows/`](.github/workflows/README.md) | GitHub Actions automation, to be added when there are checks and build targets to run. |

## Getting started

### Prerequisites

For development once the application code is introduced, install:

- Git
- Python (version to be selected when the backend is initialized)
- Node.js and npm (version to be selected when the frontend is initialized)
- PostgreSQL

AI model runtimes and model files will be documented when the AI services are implemented. Model files and other large/generated assets should not be committed.

### Prepare local configuration

1. Copy `.env.example` to `.env` at the repository root.
2. Set local PostgreSQL connection values in `.env`. Keep real credentials in this local file or a secrets manager; never commit them.
3. Start or connect to a local PostgreSQL instance and create the configured development database.

For PowerShell:

```powershell
Copy-Item .env.example .env
```

This scaffold does not yet include frontend or backend dependency manifests, database migrations, or application entry points, so there are no install or run commands at this stage. Those commands should be added alongside the corresponding implementation.

## Configuration

`.env.example` lists the anticipated local configuration keys without containing production credentials. The application does not yet load these values. Update the example when configuration requirements become concrete, and document any new variable where it is introduced.

## Development principles

- Keep frontend, backend, and AI service responsibilities clearly separated.
- Treat PostgreSQL migrations as the source of truth for schema changes.
- Keep secrets, local environment files, model weights, and generated outputs out of version control.
- Add automated checks when their respective build and test commands exist.
