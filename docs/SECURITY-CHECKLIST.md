# Security Checklist

- [ ] Production secrets are outside Git.
- [ ] PostgreSQL and Redis are private-network only.
- [ ] TLS is enabled for all public traffic.
- [ ] Strong password hashing and JWT/refresh-token rotation are enabled and tested.
- [ ] Tenant/branch authorization is tested for every data-access path.
- [ ] Rate limits are configured for authentication and sensitive endpoints.
- [ ] Audit logs are immutable enough for the operational threat model.
- [ ] Backups are encrypted and restore-tested.
- [ ] Electron Windows installers are Authenticode signed.
- [ ] License private key is never shipped to clients.
- [ ] Dependencies are pinned/locked and scanned in CI.
- [ ] Database migrations are reviewed before production deployment.
- [ ] Error responses do not leak secrets, SQL, tokens or PII.
- [ ] Monitoring and alerting cover API errors, latency, DB health, disk and certificate expiry.
