# MEDORAX Admin ↔ ERP integration contract

The onboarding/admin control plane provisions the ERP through the protected internal endpoint:

`POST /internal/erp/provision`

The ERP accepts the signed license envelope and the onboarding-issued ERP username/temporary password. The ERP never accepts a license issuer private key and never issues commercial licenses itself.

## Provisioning payload

Required business fields are tenant/pharmacy identity, ERP username, temporary password, and the signed `license` + `signature` envelope. The license must have product `MEDORAX-ERP`, matching tenant ID, and a valid signature.

## Expected response

The response includes the ERP user/external ID and provisioning status. Admin should persist the returned external ID against the onboarding application.

## Retry

Admin may retry an approved application when an ERP installation/database was reset. A retry reuses the existing approved credentials and signed license; it does not silently issue a second license.

## Login

The customer logs into the ERP using the provisioned ERP username and temporary password. ERP login is license-gated and device-bound. Central licensing validation remains authoritative for activation/revocation/expiry.
