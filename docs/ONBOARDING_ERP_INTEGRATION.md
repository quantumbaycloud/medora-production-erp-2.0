# MEDORAX Onboarding → ERP integration

## Production contract

1. Admin approves an onboarding application.
2. The onboarding admin API issues a signed `MEDORAX-ERP` Ed25519 license from the private licensing issuer.
3. The admin API generates the ERP username and a temporary password, stores only an encrypted copy, and calls the ERP internal endpoint.
4. ERP `/internal/erp/provision` verifies:
   - the provisioning bearer token;
   - license signature;
   - `license_id`/tenant consistency;
   - license product and expiry;
   - username uniqueness;
   - tenant/pharmacy ownership.
5. ERP creates/updates the user credential and tenant, installs the signed license, and returns its ERP user/pharmacy IDs.
6. Customer signs into ERP using the onboarding-provided username + temporary password (email/phone remain accepted for legacy accounts).
7. ERP authentication is license-gated. The first login automatically activates the browser/device against the provisioned license. Later protected requests continue to enforce license status, expiry, revocation and the configured offline grace period.

## Shared secrets

The onboarding admin API and onboarding API must use the same `FIELD_ENCRYPTION_KEY`, because the temporary ERP password is encrypted by admin-api and decrypted by onboarding-api for the customer's dashboard.

The ERP API and onboarding admin API must share the same `ERP_PROVISION_TOKEN` value. The onboarding admin API must use the ERP internal provisioning URL; the ERP API must never expose `/internal/erp/*` through a public reverse proxy.

The ERP API and licensing issuer must share the issuer URL/token and the ERP must have the issuer's public Ed25519 key mounted read-only.

## Local test order

- Start the ERP Postgres, Redis and licensing issuer.
- Run ERP Alembic migrations.
- Start ERP API and ERP web.
- Start onboarding Postgres and the onboarding/admin services against the same onboarding database.
- Configure onboarding admin `ERP_PROVISION_URL` to the local ERP internal endpoint and `ERP_PROVISION_TOKEN` to the same value as ERP.
- Configure the onboarding/admin and onboarding API `FIELD_ENCRYPTION_KEY` to the same Fernet key.
- Approve a test application with a verified payment/subscription.
- Confirm the onboarding dashboard displays the generated ERP username and temporary password.
- Sign into ERP with those credentials.
- Confirm ERP creates a device activation and `/api/licensing/status` reports `active`.
- Disable/expire the license and verify protected ERP APIs return `403`.

Never put production passwords, issuer private keys, Fernet keys or provisioning tokens into Git.
