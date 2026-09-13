# MEDORAX ERP API contract

All customer-facing ERP endpoints require a Bearer access token and an active licensed device unless explicitly documented as health or internal provisioning endpoints.

## Core resources

- `/auth/*` — authentication, refresh, sessions and devices
- `/users/*` — current user profile
- `/pharmacies/*` — pharmacy and branches
- `/medicines/*` — medicine catalog and batches
- `/inventory/*` — stock ledger, adjustments and import/export
- `/suppliers/*` — suppliers
- `/purchases/*` — purchase invoices
- `/billing/*` — invoicing, holds, returns, exchanges and printing
- `/api/customers/*` — customers
- `/reports/*` — dashboard and statutory reports
- `/staff/*` — staff, roles and attendance
- `/notifications/*` — alerts
- `/audit-logs` and `/documents/*` — compliance records
- `/settings/*` — pharmacy settings
- `/api/licensing/*` — ERP-side license/device operations
- `/internal/erp/*` — protected onboarding/admin provisioning

The frontend must use these APIs rather than embedded demo records.


## Production routing

Production ERP clients use `https://api.medorax.in` for all ERP API requests. The public ERP UI is `https://erp.medorax.in`.

The Electron Windows client loads `https://erp.medorax.in` and does not embed server credentials or licensing private keys.

For the complete production routing and Admin synchronization contract, see `docs/UNIFIED_ERP_API.md`.
