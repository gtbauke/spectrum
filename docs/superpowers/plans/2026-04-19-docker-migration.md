# Docker Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fully containerize the Spectrum platform, including backend, frontend, and three specialized worker types, supporting both local development and production environments.

**Architecture:** A unified Multi-stage Dockerfile at the root will handle all Python services. Docker Compose will orchestrate the full stack, including a dedicated migration service. Scripted wrappers (`dev.sh`) will manage environment-specific configurations.

**Tech Stack:** Docker, Docker Compose, Python 3.13, UV, React, Vite, PostgreSQL, RabbitMQ.

---

### Task 1: Refactor Worker Entrypoint for Granularity

**Files:**
- Modify: `packages/workers/main.py`

- [ ] **Step 1: Implement Worker Type Filtering**
Update `main.py` to read `WORKER_TYPE` environment variable and only start relevant consumers.

```python
import os
# ... existing imports ...

async def main() -> None:
    setup_logging()
    settings = Settings()
    worker_type = os.getenv("WORKER_TYPE", "all").lower()

    # ... connection setup ...

    tasks = []
    if worker_type in ("training", "all"):
        training_consumer = AioPikaConsumer(...)
        tasks.append(training_consumer.start())
    
    if worker_type in ("verification", "all"): # validation queue
        validation_consumer = AioPikaConsumer(...)
        tasks.append(validation_consumer.start())
        
    if worker_type in ("iql", "all"): # inference queue
        inference_consumer = AioPikaConsumer(...)
        tasks.append(inference_consumer.start())

    await asyncio.gather(*tasks)
```

- [ ] **Step 2: Commit worker changes**
`git add packages/workers/main.py && git commit -m "refactor: support granular worker types via env var"`

---

### Task 2: Create Unified Python Dockerfile

**Files:**
- Create: `Dockerfile` (root)
- Create: `.dockerignore` (root)

- [ ] **Step 1: Write Root Dockerfile**
Uses `uv` workspaces to optimize build.

```dockerfile
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS base
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

FROM base AS deps
COPY pyproject.toml uv.lock ./
COPY packages/backend/pyproject.toml ./packages/backend/
COPY packages/core/pyproject.toml ./packages/core/
COPY packages/db_core/pyproject.toml ./packages/db_core/
COPY packages/inference_query_language/pyproject.toml ./packages/inference_query_language/
COPY packages/workers/pyproject.toml ./packages/workers/
RUN uv sync --frozen --no-install-project --no-dev

FROM deps AS build
COPY . /app
RUN uv sync --frozen --no-dev

FROM build AS production
ENTRYPOINT ["uv", "run"]
```

- [ ] **Step 2: Write Root .dockerignore**
Exclude local venv and data.

```text
.venv
__pycache__
node_modules
spectrum_data
*.egg-info
.git
```

- [ ] **Step 3: Commit Dockerfile**
`git add Dockerfile .dockerignore && git commit -m "feat: add unified python dockerfile"`

---

### Task 3: Configure Docker Compose for Multi-Service Orchestration

**Files:**
- Modify: `docker-compose.yml`

- [ ] **Step 1: Define full stack in Compose**
Add services for all workers and the backend, plus the migration runner.

```yaml
services:
  postgres:
    image: postgres:16
    container_name: spectrum-postgres
    # ... healthcheck ...

  rabbitmq:
    image: rabbitmq:3.13-management
    container_name: spectrum-rabbitmq

  migration:
    build: .
    depends_on:
      postgres: { condition: service_healthy }
    command: ["uv", "run", "--package", "db-core", "alembic", "upgrade", "head"]
    env_file: .env

  backend:
    build: .
    ports: ["8000:8000"]
    depends_on:
      migration: { condition: service_completed_successfully }
      rabbitmq: { condition: service_healthy }
    command: ["uv", "run", "--package", "backend", "fastapi", "run", "packages/backend/app/main.py"]
    volumes: ["./packages:/app/packages"] # dev only

  worker-training:
    build: .
    environment: { WORKER_TYPE: "training" }
    depends_on: [rabbitmq]
    command: ["python", "packages/workers/main.py"]

  # ... other workers ...

  frontend:
    build: ./packages/frontend
    ports: ["5173:5173"]
    # ...
```

- [ ] **Step 2: Commit Compose changes**
`git add docker-compose.yml && git commit -m "feat: expand docker-compose to include app services"`

---

### Task 4: Update Frontend for Docker

**Files:**
- Modify: `packages/frontend/Dockerfile`

- [ ] **Step 1: Support VITE_API_BASE_URL build arg**
- Ensure production build uses correct API.

- [ ] **Step 2: Commit Frontend changes**
- `git commit -m "feat: update frontend dockerfile for production builds"`

---

### Task 5: Refactor dev.sh to use Docker

**Files:**
- Modify: `scripts/dev.sh`

- [ ] **Step 1: Replace local processes with Docker Compose**
Update the script to handle environment patching (localhost -> container name) and then call `docker compose up`.

- [ ] **Step 2: Commit script changes**
`git commit -m "refactor: dev.sh now orchestrates via docker compose"`

---

### Task 6: Verification

- [ ] **Step 1: Run fresh dev environment**
`./scripts/dev.sh`
- [ ] **Step 2: Verify all workers are connected**
Check RabbitMQ management UI or logs.
- [ ] **Step 3: Verify Persistence**
Create a record, restart containers, check if it's still there.
