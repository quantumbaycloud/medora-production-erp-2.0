# MEDORAX ERP production deployment

## Domains

- ERP UI: `https://erp.medorax.in`
- ERP API: `https://erp-api.medorax.in`
- Onboarding + central licensing control plane: `https://api.medorax.in`

The ERP API must never expose the licensing issuer administration token or private signing key.

## Required production secrets

Set these in the server-side `deploy/erp-api.env` (or your secret manager):

- `DATABASE_URL`
- `JWT_SECRET` (long random value)
- `ERP_PROVISION_TOKEN` — must exactly match the onboarding Admin API provisioning token
- `LICENSE_PUBLIC_KEY_FILE=/run/secrets/medorax-license/public.pem`
- `LICENSE_ISSUER_URL=https://api.medorax.in/licensing`
- SMTP/Resend settings for production email if used
- storage credentials if document storage is enabled

`LICENSE_ISSUER_TOKEN` is intentionally empty in an ERP installation.

## Deployment

1. Install Docker Engine + Compose.
2. Place the repository on the ERP server.
3. Put the production public Ed25519 key at:
   `local-secrets/licensing/public.pem`
4. Create the production env file with strong secrets.
5. Verify:
   `docker compose -f docker-compose.prod.yml config`
6. Build:
   `docker compose -f docker-compose.prod.yml build`
7. Start:
   `docker compose -f docker-compose.prod.yml up -d`
8. Check:
   `docker compose -f docker-compose.prod.yml ps`
9. Check:
   `docker compose -f docker-compose.prod.yml logs --tail=100 erp-api`
10. Verify API health:
    `GET https://erp-api.medorax.in/health/live`
    `GET https://erp-api.medorax.in/health/ready`
11. Verify UI:
    `https://erp.medorax.in`

## Onboarding -> ERP contract

The onboarding control plane calls:

`POST /internal/erp/provision`

with the existing Bearer provisioning token and the exact:

- `erpUsername`
- `temporaryPassword`
- `licenseKey`
- `license`
- `licenseSignature`
- `licenseExpiresAt`
- pharmacy/business/user data

The ERP verifies the Ed25519 signature locally and stores the signed license envelope. It hashes the onboarding password with Argon2; plaintext passwords are never persisted.

On the user's first login, the ERP automatically activates the signed license for the persisted browser/device UUID against the central licensing issuer. Subsequent logins validate the existing activation. If the issuer is temporarily unavailable, the ERP permits access only until `LICENSE_OFFLINE_GRACE_HOURS` has elapsed since the last successful validation.

## Important migration note

This repository historically bootstraps tables with SQLAlchemy `create_all()` for compatibility with the local test installation. Before production rollout, inspect the target database's current Alembic state and migration history. Do not run destructive commands or recreate the database to install this build. Use an explicit, reviewed Alembic migration plan for any schema changes.
