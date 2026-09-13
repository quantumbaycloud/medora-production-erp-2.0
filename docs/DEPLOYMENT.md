# Production Deployment

1. Provision Linux host or managed container platform.
2. Provision managed PostgreSQL and Redis where possible.
3. Create DNS records for `erp.medorax.in` and `api.medorax.in`.
4. Install TLS certificates; mount them under `ops/tls` or terminate TLS at a managed load balancer.
5. Create `deploy/erp-api.env` and `deploy/licensing-issuer.env` from the examples with strong secrets.
6. Generate/store the Ed25519 licensing private key outside Git. Mount it into the issuer as a secret.
7. Run `scripts/deploy-production.sh`.
8. Verify `/health/live` and `/health/ready` on the API through the trusted network/proxy.
9. Configure daily encrypted PostgreSQL backups and periodically test restore.
10. Configure centralized logs, metrics, alerts and certificate renewal.

Do not expose PostgreSQL, Redis, or the licensing issuer directly to the Internet.
