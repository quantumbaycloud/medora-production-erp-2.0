#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo '[1/5] Validate production compose'
docker compose -f docker-compose.prod.yml config >/dev/null

echo '[2/5] Pull/build images'
docker compose -f docker-compose.prod.yml build

echo '[3/5] Start infrastructure and licensing issuer'
docker compose -f docker-compose.prod.yml up -d postgres redis licensing-issuer

echo '[4/5] Run ERP database migrations'
docker compose -f docker-compose.prod.yml run --rm erp-api alembic upgrade head

echo '[5/5] Start ERP application'
docker compose -f docker-compose.prod.yml up -d erp-api erp-web

docker compose -f docker-compose.prod.yml ps
