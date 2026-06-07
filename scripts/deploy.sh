#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "🚀 Starting deployment for Spectrum Platform..."


echo "📥 Pulling latest code from repository..."
git pull origin main # Change 'main' to your actual branch name if different

echo "🏗️ Building and recreating Docker containers..."
# The --build flag ensures the FastAPI and SSR Node images get the fresh code
# The -d flag keeps them running in the background
docker compose -f docker-compose.prod.yml up -d --build

echo "🧹 Cleaning up old Docker images..."
# This is crucial for OCI Free Tier to prevent disk space exhaustion
docker image prune -f

echo "✅ Deployment completed successfully! Spectrum is up to date."
