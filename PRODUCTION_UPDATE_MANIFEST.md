MEDORAX ERP PRODUCTION UPDATE

Scope:
- Commercial ERP is provisioned-only; no self-registration.
- Login endpoint remains the ERP entry point and validates onboarding-provisioned licensing automatically.
- Manual license-key activation removed from ERP UI.
- Authenticated password change implemented.
- Prescription upload/checkout wired to backend APIs.
- Runtime ERP data remains API-sourced; no seeded customer/business data.
- Production secrets/endpoints are environment-driven.

Apply by copying the changed files over the existing ERP checkout and rebuilding backend/frontend.
