# MEDORAX Unified ERP API

## Production endpoints

- ERP frontend: `https://erp.medorax.in`
- ERP API: `https://api.medorax.in`
- Central Admin/Onboarding API: `https://api.medorax.in`
- Central license issuer protocol: `https://api.medorax.in/licensing`
- Unified API documentation is served by the control-plane `unified-docs` service.

## Authentication

Protected ERP APIs use:

```http
Authorization: Bearer <access_token>
```

The ERP device identity is established during login and license activation. Customer-facing ERP endpoints must not accept Admin provisioning secrets.

## API groups

| Group | Production prefix |
|---|---|
| Authentication | `/auth/*` |
| Users | `/users/*` |
| Pharmacy / branches | `/pharmacies/*`, `/branches/*` |
| Medicines | `/medicines/*` |
| Inventory | `/inventory/*` |
| Suppliers | `/suppliers/*` |
| Purchases | `/purchases/*` |
| Billing | `/billing/*` |
| Customers | `/api/customers/*` |
| Reports | `/reports/*` |
| Staff | `/staff/*` |
| Notifications | `/notifications/*` |
| Audit | `/audit-logs` |
| Documents | `/documents/*` |
| Settings | `/settings/*` |
| ERP licensing | `/api/licensing/*` |
| ERP/Admin synchronization | `/admin-sync/catalog` |
| Protected ERP provisioning | `/internal/erp/*` |

## Admin synchronization

The ERP performs an outbound server-to-server request:

```text
ERP API -> https://api.medorax.in/api/erp-sync/{pharmacy_id}/catalog
```

It sends:

```http
X-ERP-License-Key: <installed-license-id>
X-ERP-License-Signature: <installed-license-signature>
```

The central Admin service validates:

1. pharmacy is approved;
2. license exists;
3. license has not expired;
4. license key matches;
5. license signature matches.

The response contains pharmacy-scoped ERP configuration options and never needs to expose the ERP license key to the browser.

## Licensing

ERP runtime license operations are under `/api/licensing/*`.

Central issuance/renewal/revocation is control-plane functionality under `/licensing/v1/*` and must not be exposed as an unauthenticated ERP UI operation.

## Health

- `/health/live` — process liveness.
- `/health/ready` — database readiness.

## Deployment rule

The browser/Electron client must call `https://api.medorax.in`. Do not ship a production build pointing to `localhost`, `127.0.0.1`, or `erp-api.medorax.in`.

The Windows Electron client opens `https://erp.medorax.in`; the web frontend then communicates with `https://api.medorax.in`.

## Offline behavior

The current commercial ERP is primarily online. Local browser storage can preserve client state, but this repository does not implement a complete offline transaction queue for every business operation. Therefore offline operation must not be advertised as full offline POS/inventory operation until such a queue and reconciliation layer is implemented.
