# Use a multi-stage Dockerfile to optimize builds for a uv monorepo
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS base

# Install runtime dependencies for symbols regression libraries if needed (e.g., g++)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1
# Copy from the cache instead of linking since it's a separate filesystem
ENV UV_LINK_MODE=copy

# --- Dependencies Stage ---
FROM base AS deps

# Copy the lockfile and workspace configuration
COPY pyproject.toml uv.lock ./

# Copy all package manifests to allow 'uv sync' to cache dependencies
COPY packages/backend/pyproject.toml ./packages/backend/
COPY packages/core/pyproject.toml ./packages/core/
COPY packages/db_core/pyproject.toml ./packages/db_core/
COPY packages/inference_query_language/pyproject.toml ./packages/inference_query_language/
COPY packages/workers/pyproject.toml ./packages/workers/

# Install dependencies without the root project to cache high-cost layers
RUN uv sync --frozen --no-install-project --no-dev

# --- Build Stage ---
FROM deps AS build

# Copy the rest of the source code
COPY . /app

# Install the project and its dependencies (no-dev for production)
RUN uv sync --frozen --no-dev

# --- Production Stage ---
FROM build AS production

# The entrypoint will be overridden by docker-compose for workers
# Default to backend for safety
ENTRYPOINT ["uv", "run"]
CMD ["--package", "backend", "fastapi", "run", "packages/backend/app/main.py", "--host", "0.0.0.0", "--port", "8000"]
