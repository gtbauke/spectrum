#!/bin/bash

echo "Starting Spectrum backend..."

uv run fastapi dev &

SERVER_PID=$!
echo "Started server with PID: ${SERVER_PID}"

uv run celery -A app.tasks.create_sr_model worker &

CELERY_PID=$!
echo "Started celery with PID: ${CELERY_PID}"
