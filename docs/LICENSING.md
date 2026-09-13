# MEDORAX Commercial Licensing

This repository contains the working licensing control plane and ERP-side enforcement. It is separate from onboarding/admin.

## Components

- `licensing-issuer/`: development/reference issuer implementation. Production ERP installations use the MEDORAX central licensing authority exposed at `https://api.medorax.in/licensing`.
- `backend/app/licensing/`: tenant-scoped ERP API for activation, deactivation, status and module entitlements.
- `frontend/src/services/licensing/`: authenticated client for the ERP licensing API.
- `frontend/src/pages/Licensing/LicenseManagement.jsx`: operational license management screen.
- `scripts/generate-license-keys.py`: development-only Ed25519 key generation.

## License lifecycle

`ISSUED -> ACTIVATED -> ACTIVE -> EXPIRED/REVOKED/DEACTIVATED`

The onboarding control plane is the license authority: it requests a license from the central issuer, receives an Ed25519-signed canonical license envelope, stores the signed envelope with the approved application, and provisions that exact envelope to ERP. The ERP backend contains only the public verification key, verifies the signature locally, binds the license to a tenant and device, and periodically asks the central issuer for current status.

ERP installations must never contain the issuer private key or issuer administration token. The issuer administration token is used only by the onboarding/admin control plane for issuance, renewal and revocation.

## API

ERP API:

- `POST /api/licensing/activate`
- `POST /api/licensing/deactivate`
- `POST /api/licensing/validate`
- `POST /api/licensing/refresh`
- `GET /api/licensing/status`
- `GET /api/licensing/modules`

Issuer API (internal/admin):

- `POST /v1/licenses` (control plane only)
- `GET /v1/licenses/{license_id}`
- `POST /v1/licenses/{license_id}/revoke`
- `POST /v1/licenses/{license_id}/renew`
- `POST /v1/activations`
- `POST /v1/activations/deactivate`
- `POST /v1/validate`

Issuer administration endpoints require `X-Issuer-Token`.

## Production requirements

Never commit `private.pem`, issuer tokens, or production credentials. Store the private key in a secret manager/HSM/KMS and mount it read-only. The issuer uses PostgreSQL for persistent state. Keep the issuer on the internal Docker/network segment and do not publish its port through public Nginx.
