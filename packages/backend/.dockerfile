FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1

WORKDIR /app

# System deps (minimal, extend if SR libs need more)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# -------------------------
# Dependencies layer
# -------------------------
FROM base AS deps

# Install uv
RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

# -------------------------
# Runtime image
# -------------------------
FROM base AS runtime

# Copy virtual env from deps
COPY --from=deps /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

COPY app ./app

EXPOSE 8000

# Default command (overridden in compose)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
