#!/usr/bin/env bash
set -euo pipefail

ONBOARDING_ROOT="${ONBOARDING_ROOT:-/opt/medorax-onboarding-final/app/medorax-final}"
ADMIN_ENV="${ADMIN_ENV:-/opt/medorax-onboarding-final/env/admin-api.env}"
NGINX_CONF="${NGINX_CONF:-$ONBOARDING_ROOT/infra/nginx/medorax.conf}"

: "${ERP_PROVISION_TOKEN:?Set ERP_PROVISION_TOKEN before running this script}"

echo "[1/5] Backing up nginx and admin env..."
sudo cp "$NGINX_CONF" "$NGINX_CONF.backup.$(date +%Y%m%d-%H%M%S)"
sudo cp "$ADMIN_ENV" "$ADMIN_ENV.backup.$(date +%Y%m%d-%H%M%S)"

echo "[2/5] Updating Admin -> ERP provisioning settings..."
sudo touch "$ADMIN_ENV"
sudo sed -i '/^ERP_PROVISION_URL=/d;/^ERP_PROVISION_TOKEN=/d;/^ERP_TIMEOUT_SECONDS=/d' "$ADMIN_ENV"
{
  echo "ERP_PROVISION_URL=https://api.medorax.in/erp/internal/erp/provision"
  echo "ERP_PROVISION_TOKEN=$ERP_PROVISION_TOKEN"
  echo "ERP_TIMEOUT_SECONDS=20"
  echo "LICENSE_ISSUER_URL=https://api.medorax.in/licensing"
} | sudo tee -a "$ADMIN_ENV" >/dev/null

echo "[3/5] Adding ERP + Admin routing to api.medorax.in..."
python3 - "$NGINX_CONF" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
text = path.read_text()
marker = "    # MEDORAX ERP + ADMIN CONTROL PLANE ROUTES"
if marker in text:
    print("Nginx routes already present; leaving them unchanged.")
    raise SystemExit

needle = "    location /licensing/ {"
if needle not in text:
    raise SystemExit("Could not find /licensing/ location in nginx config.")

snippet = """    # MEDORAX ERP + ADMIN CONTROL PLANE ROUTES
    location ^~ /erp/ {
        proxy_pass http://127.0.0.1:8200/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 60s;
        proxy_send_timeout 60s;
    }

    location ^~ /api/admin/ {
        proxy_pass http://127.0.0.1:8010;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location ^~ /api/erp-sync/ {
        proxy_pass http://127.0.0.1:8010;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

"""
text = text.replace(needle, snippet + needle, 1)
path.write_text(text)
PY

echo "[4/5] Rebuilding Admin API and restarting onboarding..."
cd "$ONBOARDING_ROOT"
docker compose -f docker-compose.prod.yml up -d --build admin-api admin-web licensing-issuer onboarding-api

echo "[5/5] Validating nginx..."
sudo nginx -t
sudo systemctl reload nginx

echo "Admin/ERP control-plane routing update complete."
