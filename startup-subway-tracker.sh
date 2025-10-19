#!/bin/bash

# Wait for Docker daemon to be ready
echo "Waiting for Docker daemon..."
until docker info >/dev/null 2>&1; do
    echo "Docker daemon not ready, waiting..."
    sleep 2
done
echo "Docker daemon is ready"

docker compose up -d

sleep 5

# Open browser
DISPLAY=:0 chromium-browser --kiosk http://localhost:8000 &
