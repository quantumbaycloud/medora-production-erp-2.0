# MEDORAX ERP — Master Data / Admin Sync Update

## Added
- Pharmacy-scoped `catalog_options` database table.
- Admin-controlled master options: supplier categories, medicine categories, payment terms, customer types, dosage forms, units.
- Signed-license authenticated Admin synchronization endpoint.
- ERP local catalog cache and sync at workspace bootstrap.
- Supplier category stored as `category_id`, plus supplier status/description.
- Supplier create/update now excludes duplicate `pharmacy_id` payload injection.
- Supplier form now uses synchronized categories and persists GST, drug license, bank details, payment terms, status and notes.
- ERP Master Data settings view.
- `/suppliers` and `/pharmacy/settings` routes are included in the current archive.

## Local DB migration
If the local database already exists, run:
`backend/sql/20260913_catalog_supplier.sql`

## Admin sync environment
Set the ERP backend:
`ADMIN_SYNC_URL=https://<your-admin-api-domain>/api`
`ADMIN_SYNC_TIMEOUT_SECONDS=10`

The ERP never receives an Admin JWT. It authenticates the machine-to-machine catalog pull using the installed license key + signed license signature.

## Important
This update does not alter onboarding approval/rejection logic. Admin approval remains the authority that provisions the ERP credentials and license.
