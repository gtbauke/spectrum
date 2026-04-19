#!/usr/bin/env bash
set -e

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "🏗 Building production images for Spectrum..."

# Build Python Unified Image
echo "Building Python services image..."
docker build \
    --target production \
    -t spectrum-python:latest \
    .

# Build Frontend Image
# Note: VITE_API_BASE_URL should be set in environment or passed here
API_URL=${VITE_API_BASE_URL:-"/api/v1"}
echo "Building Frontend image with API_URL=$API_URL..."
docker build \
    --build-arg VITE_API_BASE_URL="$API_URL" \
    -t spectrum-frontend:latest \
    ./packages/frontend

echo "✅ Production images built successfully:"
docker images | grep spectrum
