#!/bin/bash

NETWORK_NAME="spectrum_default"

echo "🛑 Bringing down the project..."
# --remove-orphans catches containers not defined in your current compose file
docker compose down --remove-orphans

echo "🔍 Checking for stubbornly in-use networks..."
# 2. Check if the network still exists despite the 'down' command
if docker network inspect "$NETWORK_NAME" >/dev/null 2>&1; then
    echo "⚠️  Network '$NETWORK_NAME' is still hanging around."

    # 3. Find any rogue containers still attached to it
    CONTAINERS=$(docker network inspect -f '{{range $k, $v := .Containers}}{{$v.Name}} {{end}}' "$NETWORK_NAME")

    if [ ! -z "$CONTAINERS" ]; then
        echo "✂️  Forcefully disconnecting rogue containers: $CONTAINERS"
        for CONTAINER in $CONTAINERS; do
            docker network disconnect -f "$NETWORK_NAME" "$CONTAINER"
        done
    fi

    # 4. Remove the network now that it's isolated
    echo "🗑️  Removing the network..."
    docker network rm "$NETWORK_NAME"
else
    echo "✅ Network already cleaned up."
fi

# (Optional) Prune all other unused dangling networks just to be safe
docker network prune -f

echo "🚀 Bringing the project back up..."
# --build ensures any code changes are pulled into the fresh images
docker compose -f docker-compose.prod.yml up -d --build

echo "🎉 Deployment complete!"
