# Release Process

1. Create a version tag.
2. Run backend tests and migrations against a disposable database.
3. Run frontend lint/build.
4. Build and sign Electron artifacts in CI.
5. Scan dependencies and container images.
6. Back up production database.
7. Apply migrations.
8. Roll out API/web/issuer.
9. Smoke test authentication, inventory, purchase, billing, reporting and license activation.
10. Record release notes and rollback image/tag.
