# 2026-04-19-docker-migration-design

## Goal
Migrate the Spectrum symbolic regression platform's infrastructure entirely to Docker, supporting both local development and production environments.

## Architecture Overview
The system will shift from a hybrid (Docker for DB/MQ, local for services) to a fully containerized setup. We will use a script-wrapped Docker Compose orchestration to manage the complexity of multiple workers and environments.

## Components

### 1. Unified Python Dockerfile (Root)
A multi-stage Dockerfile to build all Python-based services (`backend`, `worker-training`, `worker-verification`, `worker-iql`).
- **Stage: base**: Installs Python 3.13-slim and `uv`.
- **Stage: deps**: Multi-package dependency synchronization using `uv` workspaces.
- **Stage: development**: Optimized for volume mounting and hot-reload.
- **Stage: production**: Bundled code for standalone execution.

### 2. Frontend Dockerfile
Refined version of the existing `packages/frontend/Dockerfile`.
- Supports `VITE_API_BASE_URL` as a build argument.
- Supports Vite dev-server mode for development via volume mounts.

### 3. Docker Compose Configuration
A unified `docker-compose.yml` defining the following services:
- **`postgres`**: Database with healthcheck.
- **`rabbitmq`**: Message broker with management UI.
- **`backend`**: FastAPI application.
- **`worker-training`**: Python worker for training tasks.
- **`worker-verification`**: Python worker for verification tasks.
- **`worker-iql`**: Python worker for inference tasks.
- **`frontend`**: React browser-based UI.
- **`migration`**: Init-container style service to run Alembic migrations.

### 4. Networking & Communication
- Dedicated internal network (`spectrum-net`) allows services to communicate via container names.
- Environment variables will be patched to use `postgres:5432` and `rabbitmq:5672` inside Docker.

### 5. Persistence
- Named Docker volumes for `postgres` and `rabbitmq` data.
- Host-mapped volume for `spectrum_data` when in local storage mode.

## Environment Management (Approach 3: Scripted Wrappers)
Two primary entry points for users:
- **`scripts/dev.sh`**: Orchestrates `docker compose` with development overrides, code volumes, and `--reload`.
- **`scripts/prod-build.sh`**: Builds production-ready images.

## Implementation Details

### Worker Granularity
The `packages/workers/main.py` will be updated to accept a `WORKER_TYPE` environment variable. This allows running separate containers for each worker type while using the same underlying code and image.

### Migration logic
The `migration` service will run as part of the startup flow in `dev.sh`. It ensures that database schemas are always up-to-date before services start.

## Verification Plan
1. **Infrastructure**: Verify that all containers start successfully and are on the same network.
2. **Persistence**: Ensure data persists across container restarts.
3. **Hot-Reload**: Verify that changing code in `packages/backend` or `packages/frontend` triggers a reload inside the container.
4. **Environment Toggle**: Verify that `STORAGE_TYPE=s3` and `STORAGE_TYPE=local` both work within the Docker network.
