# MEDORAX ERP — Commercial Central Licensing Update

## Architecture
- Onboarding/admin is the licensing control plane.
- The central issuer is `https://api.medorax.in/licensing`.
- Onboarding receives a signed Ed25519 license envelope and provisions that exact envelope to ERP.
- ERP verifies the signature locally using only the public key, then activates/validates the device with the central issuer.
- ERP installations do not contain the issuer private key or issuer administration token.
- The ERP production API is `https://api.medorax.in/erp`; `api.medorax.in` remains the onboarding/licensing control-plane host.

## Local test
1. Run `python scripts/generate-license-keys.py` once for local development.
2. Run `scripts/local-bootstrap.ps1` on Windows, or `bash scripts/local-bootstrap.sh` on Linux/macOS.
3. The local stack uses a local licensing issuer and the normal ERP provisioning contract; it never contacts production Admin for local bootstrap.
4. On first login, ERP automatically activates the provisioned signed license for the current device.

## Production deployment
- Configure DNS/TLS for `erp.medorax.in` to the ERP web server and keep `api.medorax.in` on the onboarding/control-plane server. Route `api.medorax.in/erp/` to the ERP API container.
- Build/restart the ERP stack with `docker-compose.prod.yml`.
- Do not copy issuer private keys or issuer admin tokens into the ERP installation.

The issuer admin token remains a control-plane secret on onboarding/admin only.


## Production-hardening changes in this build
- Onboarding provisioning remains the authoritative source of ERP username, temporary password and signed license.
- Provisioning validates the signed license expiration against `licenseExpiresAt` before changing ERP state.
- Every onboarding credential rotation updates `password_updated_at` and revokes existing ERP sessions.
- ERP login resolves `erpUsername`, email or mobile number and requires the tenant's provisioned license.
- The same persisted client device UUID is used by authentication and licensing.
- Central license validation is fail-closed: unknown issuer/network states do not grant UI access; the configured offline grace period is the only outage allowance.
- ERP installations never receive the central licensing issuer administration token or private signing key.
- Frontend API requests automatically rotate access tokens once on a 401 and retry the original request.
- Production health checks are included for the ERP API.
- Production CORS remains environment-controlled; do not deploy with a wildcard origin.
