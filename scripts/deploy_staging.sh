#!/bin/bash

# Stop and remove old containers
docker compose -f docker-compose.staging.yml down

# Pull the latest images
# docker pull devshittu/mediaapp:frontend-latest
docker pull devshittu/mediaapp:web-app-latest

# Start the containers with the new images
docker compose -f docker-compose.staging.yml up -d

# scripts/deploy_staging.sh