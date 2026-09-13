# Architecture

```text
                         Internet
                            |
                   +----------------+
                   | Nginx / TLS    |
                   +-------+--------+
                       |       |
              erp.medorax.in  api.medorax.in
                       |       |
                    ERP Web  ERP API
                       |       |
                       +---+---+
                           |
                +----------+----------+
                |                     |
             PostgreSQL             Redis
                |
        backups / PITR

              Internal only
                    |
             Licensing Issuer
                    |
             Ed25519 signing key
```

## Applications
- `frontend/`: React/Vite ERP web application.
- `electron/`: secure desktop shell; no Node integration in renderer.
- `backend/`: FastAPI ERP application and domain modules.
- `licensing-issuer/`: isolated license issuance service.

## Domain modules already represented by the supplied ERP backend
Authentication, users, pharmacy, branches, staff/RBAC, medicine, suppliers, purchasing, inventory, customers,
billing, audit, notifications, reports, settings and prescriptions.
