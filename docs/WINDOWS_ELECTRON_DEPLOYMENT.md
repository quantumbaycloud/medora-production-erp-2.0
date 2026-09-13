# MEDORAX ERP Windows Electron deployment

## Product model

The Windows application is a signed Electron client for the production ERP at:

`https://erp.medorax.in`

The browser UI communicates with:

`https://api.medorax.in`

The Windows client is not a standalone offline database application. Business data and authentication remain server-backed.

## Build

From `frontend/`:

```powershell
npm ci
npm run dist
```

Output:

`frontend/release/MEDORAX-ERP-2.0.0-Setup.exe`

## Production safety

- Never package `.env` files or server secrets into Electron.
- Never package Admin JWT secrets, ERP provisioning tokens, issuer tokens, database passwords, or license private keys.
- Production API URL is compiled as `https://api.medorax.in`.
- Production UI URL is `https://erp.medorax.in`.
- Only HTTPS production navigation to `erp.medorax.in` is permitted by the Electron shell.
- Code-sign the generated installer and executable before customer distribution.

## Online/offline

The current product is online-first. A temporary Internet outage can prevent login, central licensing operations, Admin synchronization, and server-backed business operations. It must not be marketed as a fully offline ERP until a complete local transaction queue/reconciliation architecture is implemented.
