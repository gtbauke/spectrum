#!/usr/bin/env bash
set -e

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ENV_FILE="$ROOT_DIR/.env"

echo "Starting Spectrum (local development)..."
echo "Project Root: $ROOT_DIR"

if [ ! -f "$ENV_FILE" ]; then
  echo "Error: .env file not found at $ENV_FILE. Please create it based on .env.example and try again."
  exit 1
fi

echo "Loading environment variables from $ENV_FILE..."
set -o allexport
source "$ENV_FILE"
set +o allexport

REQUIRED_VARS=(
    DATABASE_URL
)

for var in "${REQUIRED_VARS[@]}"; do
  if [ -z "${!var}" ]; then
    echo "Error: Environment variable '$var' is not set. Please check your .env file."
    exit 1
  fi
done

if ! command -v uv > /dev/null 2>&1; then
  echo "Error: 'uv' command not found. Please install uv with: `pip install uv`"
  exit 1
fi

cleanup() {
    echo ""
    echo "Shutting down Spectrum..."
    docker compose down
    kill $(jobs -p) 2>/dev/null || true
    clear
    exit 0
}

trap cleanup SIGINT SIGTERM

if nc -z localhost 5432 2>/dev/null; then
    echo "⚠️  Local Postgres detected on port 5432"

    if command -v systemctl > /dev/null; then
        echo "🛑 Stopping Postgres via systemctl"
        sudo systemctl stop postgresql || true
        sudo systemctl stop postgresql@* || true
    else
        echo "⚠️  systemctl not found, skipping Postgres stop"
    fi
else
    echo "✅ No local Postgres running"
fi

MIGRATION_MESSAGE="$1"

if [ -z "$MIGRATION_MESSAGE" ]; then
  echo "Usage: $0 \"migration message\""
  exit 1
fi

echo "Starting Postgres with Docker Compose..."
(
    cd "$ROOT_DIR"
    docker compose up -d --build postgres
)

echo "Waiting for Postgres and RabbitMQ to be ready..."
until docker exec spectrum-postgres pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB" > /dev/null 2>&1; do
    echo "Waiting for Postgres to be ready..."
    sleep 1
done

echo "✅ Postgres is ready!"
echo "You can now create your migration"

cd "$ROOT_DIR/packages/db_core"
uv run alembic revision --autogenerate -m "$MIGRATION_MESSAGE"

docker compose down
cd "$ROOT_DIR"

echo "Migration created successfully! Don't forget to apply it with: uv run alembic upgrade head"

