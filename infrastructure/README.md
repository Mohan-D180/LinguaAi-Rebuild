# Local Docker development

The root `compose.yaml` starts the Vite frontend, FastAPI backend, and PostgreSQL on a private Compose bridge network. Only the frontend is published to the host, bound to `127.0.0.1:5173`. The backend and database are reachable to other services by their Compose names and are not exposed on host ports.

The Vite development server proxies `/api` requests to the backend. From the browser or host, check the API through `http://localhost:5173/api/v1/health`; check PostgreSQL connectivity through `http://localhost:5173/api/v1/health/database`. Compose waits for PostgreSQL to pass `pg_isready` before starting the backend, and for the backend health check before starting the frontend.

## Requirements

- Docker Engine or Docker Desktop with the Compose plugin
- BuildKit support (enabled by default in current Docker releases)

Run commands from the repository root.

## Start and inspect

```powershell
Copy-Item .env.example .env
# Replace the development-only POSTGRES_PASSWORD and keep the values in .env.
docker compose up --build
```

Open [http://localhost:5173](http://localhost:5173). In another terminal:

```powershell
docker compose ps
docker compose logs -f frontend backend
Invoke-RestMethod http://localhost:5173/api/v1/health
Invoke-RestMethod http://localhost:5173/api/v1/health/database
```

Apply migrations from the backend container:

```powershell
docker compose exec backend alembic upgrade head
```

The root `.env` supplies `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `DATABASE_URL`. Keep the credentials and URL aligned; URL-encode special characters in the URL password. Compose passes these values at runtime, not into the image.

Stop and remove the containers and Compose network:

```powershell
docker compose down
```

To also remove the named frontend dependency, npm cache, and PostgreSQL data volumes:

```powershell
docker compose down --volumes
```

PostgreSQL data is stored in the `postgres_data` named volume and survives container recreation and `docker compose down`. `docker compose down --volumes` deliberately deletes that data. The backend and frontend source directories are bind-mounted for live reload. Frontend `node_modules` and npm's package cache use named volumes so host dependencies are not copied into the containers. Backend package downloads use a BuildKit cache mount during image builds. Rebuild after changing either dependency manifest:

```powershell
docker compose up --build
```

Set `BACKEND_LOG_LEVEL` or `BACKEND_CORS_ORIGINS` in the shell or a root `.env` file to override the Compose development defaults. Do not put production credentials in images or commit local environment files. Redis and AI model services are not included.

## Docker concepts used here

- **Image:** A built, versioned filesystem and configuration used as a template for a service.
- **Container:** A running instance of an image. Compose manages one frontend and one backend container.
- **Volume:** Persistent storage managed by Docker. Named frontend volumes preserve installed Node dependencies and npm's package cache; `postgres_data` preserves PostgreSQL data across container recreation.
- **Network:** The private bridge network lets Compose services find each other by service name. Backend and PostgreSQL ports are available on this network but not published to the host.
- **Compose:** A declarative configuration and command-line tool that builds, connects, starts, health-checks, and stops the related services together.
