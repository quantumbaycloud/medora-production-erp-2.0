$ErrorActionPreference = "Stop"

if (-not (Test-Path "local-secrets/licensing/public.pem")) {
  python scripts/generate-license-keys.py
}

$issuerToken = if ($env:LOCAL_LICENSE_ISSUER_TOKEN) { $env:LOCAL_LICENSE_ISSUER_TOKEN } else { "local-only-issuer-token-change-me" }
$provisionToken = "local-only-provision-token-change-me"

docker compose -f docker-compose.local.yml up -d postgres redis licensing-issuer erp-api erp-web
docker compose -f docker-compose.local.yml run --rm `
  -e LICENSE_ISSUER_TOKEN=$issuerToken `
  -e ERP_PROVISION_TOKEN=$provisionToken `
  erp-api python -m app.dev_bootstrap

Write-Host "Local ERP: http://localhost:5173"
