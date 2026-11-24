# Local Docker development

The root `compose.yaml` starts the Vite frontend and FastAPI backend on a private Compose bridge network. Only the frontend is published to the host, bound to `127.0.0.1:5173`. The backend is reachable by the frontend container as `http://backend:8000` and is not exposed on a host port.

The Vite development server proxies `/api` requests to the backend. From the browser or host, check the API through `http://localhost:5173/api/v1/health`. The backend also has an internal container health check; Compose waits for it before starting the frontend.

## Requirements

- Docker Engine or Docker Desktop with the Compose plugin
- BuildKit support (enabled by default in current Docker releases)

Run commands from the repository root.

## Start and inspect

```powershell
docker compose up --build
```

Open [http://localhost:5173](http://localhost:5173). In another terminal:

```powershell
docker compose ps
docker compose logs -f frontend backend
Invoke-RestMethod http://localhost:5173/api/v1/health
```

Stop and remove the containers and Compose network:

```powershell
docker compose down
```

To also remove the named frontend dependency and npm cache volumes:

```powershell
docker compose down --volumes
```

The backend and frontend source directories are bind-mounted for live reload. Frontend `node_modules` and npm's package cache use named volumes so host dependencies are not copied into the containers. Backend package downloads use a BuildKit cache mount during image builds. Rebuild after changing either dependency manifest:

```powershell
docker compose up --build
```

Set `BACKEND_LOG_LEVEL` or `BACKEND_CORS_ORIGINS` in the shell or a root `.env` file to override the Compose development defaults. Do not put production credentials in images or commit local environment files. No database, Redis, or AI model services are included.

## Docker concepts used here

- **Image:** A built, versioned filesystem and configuration used as a template for a service.
- **Container:** A running instance of an image. Compose manages one frontend and one backend container.
- **Volume:** Persistent storage managed by Docker. Named frontend volumes preserve installed Node dependencies and npm's package cache across container recreation.
- **Network:** The private bridge network lets Compose services find each other by service name. The backend port is available on this network but not published to the host.
- **Compose:** A declarative configuration and command-line tool that builds, connects, starts, health-checks, and stops the related services together.
