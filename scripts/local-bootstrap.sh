#!/usr/bin/env bash
set -euo pipefail

if [[ ! -f local-secrets/licensing/public.pem ]]; then
  python3 scripts/generate-license-keys.py
fi

ISSUER_TOKEN="${LOCAL_LICENSE_ISSUER_TOKEN:-local-only-issuer-token-change-me}"
PROVISION_TOKEN="${ERP_PROVISION_TOKEN:-local-only-provision-token-change-me}"

docker compose -f docker-compose.local.yml up -d postgres redis licensing-issuer erp-api erp-web
docker compose -f docker-compose.local.yml run --rm \
  -e LICENSE_ISSUER_TOKEN="$ISSUER_TOKEN" \
  -e ERP_PROVISION_TOKEN="$PROVISION_TOKEN" \
  erp-api python -m app.dev_bootstrap

echo "Local ERP: http://localhost:5173"
