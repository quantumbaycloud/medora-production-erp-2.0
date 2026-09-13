# MEDORAX ERP ↔ Onboarding/Admin Production Contract

This ERP is a provisioned commercial client. It does **not** self-register accounts and it does not accept customer-entered license keys.

## Authentication

| Method | Endpoint | Purpose | Source of account data |
|---|---|---|---|
| POST | `/auth/login` | Sign in with provisioned ERP username/email/mobile + password | Onboarding/Admin provisioning |
| POST | `/auth/refresh` | Rotate access token | ERP session |
| POST | `/auth/logout` | End current session | ERP session |
| POST | `/auth/logout-all` | Revoke other sessions | ERP session |
| GET | `/auth/me` | Current user | ERP database |
| POST | `/auth/change-password` | Authenticated user password change | ERP database; does not create an account |
| GET | `/auth/sessions` | Session list | ERP database |
| DELETE | `/auth/sessions/{session_id}` | Revoke session | ERP database |
| GET | `/auth/devices` | Device list | ERP database |
| PATCH | `/auth/devices/{device_id}` | Update device metadata | ERP database |
| POST | `/auth/devices/{device_id}/deactivate` | Deactivate device | ERP database |
| GET | `/auth/login-history` | Login audit history | ERP database |

Self-service `/auth/register`, email verification and password-reset flows are not part of the commercial ERP client surface. Credentials are created/rotated by the onboarding control plane.

## Onboarding → ERP provisioning

| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| POST | `/internal/erp/provision` | `Authorization: Bearer ERP_PROVISION_TOKEN` | Idempotently provision tenant, owner credential, pharmacy and signed license |
| GET | `/internal/erp/health` | `Authorization: Bearer ERP_PROVISION_TOKEN` | Provisioning connectivity check |

The provisioning payload must contain `pharmacyId`, `erpUsername`, `temporaryPassword`, `licenseKey`, `licenseExpiresAt`, `license`, `licenseSignature`, user and business data. The ERP verifies the signed license before committing provisioning.

## Commercial licensing

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/licensing/status` | Current tenant/device license status |
| GET | `/api/licensing/provisioned` | Provisioned-license state |
| POST | `/api/licensing/bootstrap-device` | Internal automatic device bootstrap; invoked by the authenticated ERP licensing flow |
| POST | `/api/licensing/refresh` | Revalidate current device license |

Customer UI must not manually enter or activate license keys. The license originates in onboarding/admin and is automatically validated during ERP login.

## Application APIs

The production ERP exposes the following functional route groups from `backend/app/main.py`: auth, users, pharmacies, branches, staff, medicines, suppliers, purchases, inventory, customers, billing, audit logs, notifications, reports, settings, prescriptions, licensing and internal provisioning. The canonical OpenAPI document is `erp-openapi.json`; `/docs` and `/openapi.json` are enabled according to deployment configuration.

## Configuration

No production endpoint, credential, license token, database password or object-storage credential is embedded in frontend source. Production values are supplied through environment/secrets.

Required production integration values include `DATABASE_URL`, `JWT_SECRET`, `CORS_ORIGINS`, `LICENSE_ISSUER_URL`, `ERP_PROVISION_TOKEN`, object-storage settings and a HTTPS `APP_BASE_URL`.

## ERP API inventory (source route map)

All application routes below require the normal authenticated/permission checks unless explicitly marked internal. The financial service is mounted under `/api`.

### Core ERP API

| Method | Path |
|---|---|
| GET | `/health/live` |
| GET | `/health/ready` |
| DELETE | `/auth/sessions/{session_id}` |
| GET | `/auth/devices` |
| GET | `/auth/login-history` |
| GET | `/auth/me` |
| GET | `/auth/sessions` |
| PATCH | `/auth/devices/{device_id}` |
| POST | `/auth/change-password` |
| POST | `/auth/devices/{device_id}/deactivate` |
| POST | `/auth/login` |
| POST | `/auth/logout` |
| POST | `/auth/logout-all` |
| POST | `/auth/refresh` |
| GET | `/users/me` |
| PATCH | `/users/me` |
| GET | `/pharmacies/mine` |
| GET | `/pharmacies/{pharmacy_id}` |
| PATCH | `/pharmacies/{pharmacy_id}` |
| POST | `/pharmacies/{pharmacy_id}/branches` |
| GET | `/pharmacies/{pharmacy_id}/branches` |
| GET | `/branches/{branch_id}` |
| PATCH | `/branches/{branch_id}` |
| PATCH | `/branches/{branch_id}/status` |
| DELETE | `/branches/{branch_id}` |
| GET | `/pharmacies/{pharmacy_id}/roles` |
| POST | `/pharmacies/{pharmacy_id}/roles` |
| PATCH | `/pharmacies/{pharmacy_id}/roles/{role_id}` |
| DELETE | `/pharmacies/{pharmacy_id}/roles/{role_id}` |
| GET | `/pharmacies/{pharmacy_id}/permissions` |
| GET | `/pharmacies/{pharmacy_id}/staff` |
| POST | `/pharmacies/{pharmacy_id}/staff` |
| GET | `/pharmacies/{pharmacy_id}/staff/{staff_id}` |
| PATCH | `/pharmacies/{pharmacy_id}/staff/{staff_id}` |
| PATCH | `/pharmacies/{pharmacy_id}/staff/{staff_id}/status` |
| POST | `/pharmacies/{pharmacy_id}/staff/{staff_id}/check-in` |
| POST | `/pharmacies/{pharmacy_id}/staff/{staff_id}/check-out` |
| GET | `/pharmacies/{pharmacy_id}/attendance` |
| PATCH | `/pharmacies/{pharmacy_id}/attendance/{attendance_id}/override` |
| GET | `/medicines/{medicine_id}` |
| GET | `/medicines/{medicine_id}/batches` |
| PATCH | `/medicines/{medicine_id}` |
| POST | `/medicines/{medicine_id}/batches` |
| GET | `/suppliers/` |
| POST | `/suppliers/` |
| GET | `/suppliers/{supplier_id}` |
| PATCH | `/suppliers/{supplier_id}` |
| PUT | `/suppliers/{supplier_id}` |
| DELETE | `/suppliers/{supplier_id}` |
| GET | `/purchases/{purchase_id}` |
| PATCH | `/purchases/{purchase_id}` |
| POST | `/purchases/{purchase_id}/approve` |
| GET | `/inventory/ledger` |
| POST | `/inventory/adjust` |
| GET | `/inventory/export/{entity}` |
| POST | `/inventory/import/medicines` |
| GET | `/api/customers/` |
| POST | `/api/customers/` |
| POST | `/billing/items` |
| POST | `/billing/invoice` |
| POST | `/billing/quick` |
| POST | `/billing/hold` |
| GET | `/billing/hold/{hold_number}` |
| POST | `/billing/returns` |
| POST | `/billing/exchanges` |
| GET | `/invoices/{invoice_number}` |
| GET | `/invoices/{invoice_number}/thermal` |
| GET | `/invoices/{invoice_number}/a4` |
| GET | `/reports/dashboard` |
| GET | `/reports/sales` |
| GET | `/reports/expiry` |
| GET | `/reports/gst` |
| GET | `/audit-logs` |
| GET | `/documents` |
| POST | `/documents/upload` |
| GET | `/documents/{document_id}/download` |
| PATCH | `/notifications/{notification_id}/read` |
| POST | `/notifications/mark-all-read` |
| GET | `/prescriptions/{prescription_id}` |
| GET | `/prescriptions/{prescription_id}/analysis` |
| POST | `/prescriptions/upload` |
| POST | `/prescriptions/allergy-warning` |
| POST | `/prescriptions/drug-interactions` |
| POST | `/prescriptions/generic-suggestions` |
| POST | `/prescriptions/{prescription_id}/human-review` |
| GET | `/settings` |
| PATCH | `/settings` |

### Commercial licensing

| Method | Path |
|---|---|
| GET | `/api/licensing/modules` |
| GET | `/api/licensing/provisioned` |
| GET | `/api/licensing/status` |
| POST | `/api/licensing/bootstrap-device` |
| POST | `/api/licensing/refresh` |
| POST | `/api/licensing/activate` | internal application endpoint; not exposed as a customer workflow |
| POST | `/api/licensing/activate-key` | retained for compatibility; not linked from the commercial ERP UI |
| POST | `/api/licensing/deactivate` | retained for administrative compatibility; not linked from the commercial ERP UI |
| POST | `/api/licensing/validate` | server-side validation |

### ERP ↔ Admin internal provisioning

| Method | Path |
|---|---|
| GET | `/internal/erp/health` |
| POST | `/internal/erp/provision` |
| POST | `/internal/cleanup` |

### Financial subsystem

Mounted under `/api`: cashbook balance/entry, bankbook balance/entry, orders/create, and payment webhooks for CCAvenue, Paytm and Razorpay, plus internal inventory/supplier synchronization.

> `/auth/register` is intentionally absent from this production ERP route inventory. Account creation remains an onboarding/admin responsibility.
