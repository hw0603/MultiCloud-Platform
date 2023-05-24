#!/usr/bin/env bash

CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"  # 현재 디렉토리 절대경로

# check is there a docker-compose command, if not, use "docker compose" instead.
if [ -x "$(command -v docker-compose)" ]; then
    dc=docker-compose
else
    dc="docker compose"
fi

exec $dc up --build -d
