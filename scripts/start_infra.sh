#!/bin/bash
set -e

CONTAINER_NAME="synapse-redis"
REDIS_PORT=6379

echo "Checking for existing Redis container..."
if podman ps -a --format "{{.Names}}" | grep -q "^${CONTAINER_NAME}$"; then
    echo "Container ${CONTAINER_NAME} exists."
    if podman ps --format "{{.Names}}" | grep -q "^${CONTAINER_NAME}$"; then
        echo "Container ${CONTAINER_NAME} is already running."
    else
        echo "Starting ${CONTAINER_NAME}..."
        podman start ${CONTAINER_NAME}
    fi
else
    echo "Creating and starting ${CONTAINER_NAME}..."
    podman run -d --name ${CONTAINER_NAME} -p ${REDIS_PORT}:6379 docker.io/library/redis:alpine
fi

echo "Redis is ready on port ${REDIS_PORT}."
