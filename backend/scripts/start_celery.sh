#!/bin/bash

echo "Starting Spectrum task runner backend..."

uv run celery -A app.tasks.create_sr_model worker --loglevel=INFO &

CELERY_PID=$!
echo "Started celery with PID: ${CELERY_PID}"
