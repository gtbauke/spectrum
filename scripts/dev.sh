#!/usr/bin/env bash
set -e

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ENV_FILE="$ROOT_DIR/.env"

echo "🚀 Starting Spectrum (Docker Development Mode)..."
echo "Project Root: $ROOT_DIR"

if [ ! -f "$ENV_FILE" ]; then
  echo "Error: .env file not found at $ENV_FILE. Please create it based on .env.example and try again."
  exit 1
fi

# Cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down Spectrum..."
    docker compose down
    exit 0
}

trap cleanup SIGINT SIGTERM

# Extract ports from .env for conflict detection
PG_PORT=$(grep POSTGRES_PORT "$ENV_FILE" | cut -d '=' -f2 || echo "5432")
RMQ_PORT=$(grep RABBITMQ_PORT "$ENV_FILE" | cut -d '=' -f2 || echo "5672")

# Check for port conflicts
CONFLICT_PORTS=("$PG_PORT" "$RMQ_PORT" 15672 8000 5173)
for port in "${CONFLICT_PORTS[@]}"; do
  if nc -z localhost "$port" 2>/dev/null; then
    echo "⚠️  Warning: Port $port is already in use by a local process. This will likely cause Docker startup failures."
    echo "   Please stop the service running on $port or change the port in your .env file."
  fi
done

echo "📦 Orchestrating services with Docker Compose..."
(
    cd "$ROOT_DIR"
    # Build and start services
    docker compose up --build
)
