# MEDORAX ERP — Commercial Production Repository

ERP-only repository for the MEDORAX pharmacy ERP. **Onboarding and admin services are intentionally not included.**

## Included

- React/Vite ERP web application
- FastAPI ERP API
- PostgreSQL + Alembic migrations
- Authentication, sessions and device management
- Pharmacy/tenant and branch management
- Staff/RBAC and attendance
- Medicine, batch and inventory management
- Suppliers and purchasing
- Customers and billing/sales
- Prescriptions
- Reports, notifications, settings and audit
- **Commercial licensing API and issuer**
- **Ed25519 license signing and verification**
- **Tenant/device activation and revocation**
- Electron desktop shell
- Production Docker/Nginx/monitoring/backup scaffolding

## Commercial licensing

The working licensing implementation is in `backend/app/licensing`, `licensing-issuer`, and `frontend/src/services/licensing`. See `docs/LICENSING.md`.

The issuer is an internal control-plane service. Do not expose it publicly. Never commit issuer private keys or production tokens.

## Local development

1. Generate development signing keys:
   `python scripts/generate-license-keys.py`
2. Configure the ERP API with `LICENSE_PUBLIC_KEY_FILE` and `LICENSE_ISSUER_URL`.
3. Start PostgreSQL and Redis.
4. Run Alembic migrations from `backend`.
5. Start the API and frontend.
6. Issue a test license from the issuer, then activate it from `/license` in the ERP.

## Production schema management

Use Alembic migrations for production database changes. The API retains a guarded `create_all()` bootstrap path for local development; PostgreSQL advisory locking prevents multiple Gunicorn workers from concurrently creating the same relation/type.


## Onboarding-provisioned ERP login

Approved onboarding accounts are provisioned with a unique ERP username and temporary password. The ERP accepts that username, email, or mobile number at `/auth/login`. ERP login is blocked unless the account has a valid provisioned MEDORAX-ERP license. On first login the current browser/device is automatically activated against that license.

See `docs/ONBOARDING_ERP_INTEGRATION.md` for the complete local and production contract.
