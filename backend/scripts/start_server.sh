#!/bin/bash

echo "Starting Spectrum backend..."

uv run fastapi dev &

SERVER_PID=$!
echo "Started server with PID: ${SERVER_PID}"
