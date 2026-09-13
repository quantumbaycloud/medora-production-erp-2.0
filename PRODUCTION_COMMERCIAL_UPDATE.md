# MEDORAX ERP Production / Commercial Update

This update converts the mock-heavy ERP presentation layer to an API-backed runtime data flow and hardens the backend for commercial deployment while preserving the working central licensing/onboarding provisioning flow.

## Replace

Copy the files in this update over the matching paths in the existing ERP repository.

## Delete

`backend/app/routers/suppliers.py` is intentionally removed because the project now uses the authenticated `backend/app/supplier/router.py`. Leaving the legacy router in place risks accidentally re-enabling an unauthenticated supplier API.

## Important

- Do not copy production secrets from this archive into source control.
- Set `APP_ENV=production`, explicit `CORS_ORIGINS`, strong JWT/internal/provision tokens, real storage credentials and `AUTO_CREATE_TABLES=false` in production.
- Run Alembic migrations as part of the production release process.
- The ERP runtime must not receive the licensing issuer private key or issuer administration token.
- Central licensing remains authoritative for activation, expiry and revocation.
