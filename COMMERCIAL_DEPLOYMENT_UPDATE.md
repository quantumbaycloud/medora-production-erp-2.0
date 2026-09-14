# MEDORAX ERP 2.0.1 — Commercial Deployment Update

This update separates the ERP runtime from the onboarding licensing control plane.

## Production architecture

- ERP frontend: `https://erp.meodrax.in`
- ERP API: `https://api.medorax.in/erp`
- Onboarding/admin control plane remains on `api.medorax.in`
- Commercial license issuer remains owned by onboarding at `https://api.medorax.in/licensing`
- ERP contains only the Ed25519 public verification key; it never contains the issuer private key or issuer administration token.
- Admin approval provisions the ERP through:
  `https://api.medorax.in/erp/internal/erp/provision`
- ERP pulls Admin master-data/catalog changes through:
  `https://api.medorax.in/api/erp-sync/{pharmacy_id}/catalog`

## Important

Do not copy old `licensing-issuer` services, private keys, or `LICENSE_ISSUER_TOKEN` into the ERP deployment.

Generate fresh production secrets on the server. Never commit production `.env` files.

## Local

```bash
docker compose -f docker-compose.local.yml up -d --build
```

Then open `http://localhost:5173`.

Local ERP still verifies commercial licenses against the onboarding issuer. It does not create a local license authority.

## Production

1. Configure `deploy/erp-api.env` with real database, JWT, storage, SMTP and provisioning secrets.
2. Run migrations from the ERP repository.
3. Start ERP:

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

4. Expose `127.0.0.1:8200` through the host nginx at `/erp/`.
5. Expose `127.0.0.1:8273` through nginx at `erp.meodrax.in`.
6. Configure Admin API with the same `ERP_PROVISION_TOKEN` and:
   `ERP_PROVISION_URL=https://api.medorax.in/erp/internal/erp/provision`
7. Keep `LICENSE_ISSUER_URL=https://api.medorax.in/licensing`.

## Electron

The packaged Windows app is pinned to `https://erp.meodrax.in` and only allows navigation to the MEDORAX ERP origin. Development uses `http://127.0.0.1:5173`.

Build:

```bash
cd frontend
npm ci
npm run dist
```

The installer is emitted under `frontend/release/`.

## Nginx

Use the snippets under `ops/nginx/` and the server helper:

`ops/server/ADMIN_AND_NGINX_UPDATE.sh`

The helper updates Admin -> ERP provisioning and the existing `api.medorax.in` routing. Review its paths before execution.
