#!/bin/bash

CONTAINER_NAME="health-data-sync-api"
NEW_IMAGE_NAME="${CONTAINER_NAME}"

# Change directory to the project root directory
#cd "$(dirname "$0")/.."

docker-compose --env-file .env up -d --build --remove-orphans