# MEDORAX ERP — Phase 1 Commercial/Production Update

## Target topology

- Local UI: `http://localhost:5173`
- Local ERP API: `http://localhost:8000`
- Local licensing issuer: `http://localhost:8101` (development only)
- Production UI: `https://erp.medorax.in`
- Production ERP API: `https://api.medorax.in/erp`
- Central onboarding/admin + production licensing issuer: `https://api.medorax.in`

## What changed

1. Local Docker now includes a development licensing issuer so the normal signed-license path can be exercised without contacting production Admin/licensing.
2. Local ERP uses the same internal provisioning contract as production; there is no ERP registration screen.
3. Added a development-only bootstrap that issues a local signed license and provisions a demo ERP account.
4. Production frontend is built against `https://api.medorax.in/erp` and enables Admin master-data synchronization.
5. Production CORS is restricted to `https://erp.medorax.in`.
6. Corrected all ERP production hostname references from the old typo to `medorax.in`.
7. Production deploy script no longer tries to start a nonexistent `nginx` Compose service; the existing host nginx remains the TLS reverse proxy.
8. Frontend nginx adds baseline security headers and immutable asset caching.

## Local run

1. From the ERP repository root run `python scripts/generate-license-keys.py`.
2. Start and provision with `scripts/local-bootstrap.ps1` on Windows, or `bash scripts/local-bootstrap.sh` on Linux/macOS.
3. Open `http://localhost:5173`.

The bootstrap prints the local ERP username, password, tenant ID and license ID. Change the defaults before sharing the local environment.

## Production reverse proxy

The existing server nginx should route:

- `api.medorax.in/erp/` -> `127.0.0.1:8200/`
- `erp.medorax.in/` -> `127.0.0.1:8273/`

The `/erp/` prefix is intentionally stripped by nginx's trailing-slash `proxy_pass`, so FastAPI continues to expose its normal `/auth`, `/api/licensing`, `/pharmacies`, etc. paths internally.

## Important

Production secrets remain outside Git. The ERP never receives the licensing issuer private key or issuer administration token. Onboarding Admin remains authoritative for production ERP provisioning and license issuance.
