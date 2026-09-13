#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo '[1/4] Pull/build images'
docker compose -f docker-compose.prod.yml build

echo '[2/4] Start infrastructure'
docker compose -f docker-compose.prod.yml up -d postgres redis

echo '[3/4] Run database migrations'
docker compose -f docker-compose.prod.yml run --rm erp-api alembic upgrade head

echo '[4/4] Start application'
docker compose -f docker-compose.prod.yml up -d erp-api erp-web licensing-issuer nginx

docker compose -f docker-compose.prod.yml ps
