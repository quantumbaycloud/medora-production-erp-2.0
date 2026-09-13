# MEDORAX License Issuer

Internal control-plane service for commercial MEDORAX ERP licenses.

## Security model
- Ed25519 signs the canonical license payload.
- The ERP backend verifies signatures using only the public key.
- Issuer private keys never belong in the Git repository.
- Issuer administration endpoints require `X-Issuer-Token`.
- Activation is bound to a tenant and device.
- Revocation and expiry are checked during validation.

## Development
Generate keys with `python scripts/generate-license-keys.py` from the repository root, then set:
- `LICENSE_KEY_DIR`
- `LICENSE_ISSUER_TOKEN`
- `LICENSE_STATE_FILE`

The JSON state file is deliberately simple for local development. For production, replace it with a managed PostgreSQL-backed store before horizontal scaling.
