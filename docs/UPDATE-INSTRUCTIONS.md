# MEDORAX ERP licensing update

This update contains only the files required for the central-license verification fix.

## Files
- `backend/app/licensing/service.py`
- `local-secrets/licensing/public.pem`

The public key is the Ed25519 public key corresponding to the production onboarding/licensing issuer private key. Never copy the issuer private key into the ERP.

## Apply
Copy these two paths into the ERP project, preserving the paths:

- `backend/app/licensing/service.py` -> `backend/app/licensing/service.py`
- `local-secrets/licensing/public.pem` -> `local-secrets/licensing/public.pem`

The existing compose files already mount `./local-secrets/licensing/public.pem` at `/run/secrets/medorax-license/public.pem` and the ERP environment already points `LICENSE_PUBLIC_KEY_FILE` there.

## Production/local checks
Inside the ERP project:

```bash
ls -l local-secrets/licensing/public.pem
openssl pkey -pubin -in local-secrets/licensing/public.pem -text -noout
```

Then rebuild/restart the ERP API so the mounted key is available to the container.
