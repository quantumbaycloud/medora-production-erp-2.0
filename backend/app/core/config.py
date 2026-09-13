"""
app/core/config.py

Application settings loaded from environment variables / .env file.

All operational parameters live here. No hardcoded values anywhere else.
This satisfies 12-Factor App principle #3 (config in the environment).
"""

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # â”€â”€ Runtime
    app_env: str = "development"

    # â”€â”€ Database â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    database_url: str = ""

    # â”€â”€ JWT â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    jwt_secret: str = "change-this-in-local-development-must-be-32-chars"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30

    # â”€â”€ Business Rules â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    email_required: bool = True
    phone_required: bool = False
    max_active_devices: int | None = None
    require_phone_verification_for_login: bool = False

    # â”€â”€ Email â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    # Provider: "console" (dev/test) | "smtp" | "resend"
    # "console" logs the token to stdout only â€” never use in production.
    email_provider: str = "console"
    email_from: str = "noreply@medorax.com"
    email_from_name: str = "Medorax"

    # SMTP settings (used when email_provider="smtp")
    smtp_host: str = "localhost"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_use_tls: bool = True
    smtp_timeout_seconds: int = 10

    # Resend settings (used when email_provider="resend")
    resend_api_key: str = ""
    resend_timeout_seconds: int = 10

    # Base URL for email link generation (e.g., verify-email links)
    # Must be set to the production domain. Example: https://app.medorax.com
    app_base_url: str = ""

    # â”€â”€ Cleanup Retention â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    # All values are thresholds: records OLDER than these values are eligible
    # for deletion. Tune per compliance / business requirements.
    cleanup_verification_token_hours: int = 48
    cleanup_password_reset_token_hours: int = 2
    cleanup_revoked_session_days: int = 30
    cleanup_login_history_days: int = 90
    # Unverified users older than this with no sessions are eligible for deletion.
    cleanup_unverified_user_days: int = 7

    # â”€â”€ Rate Limiting â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    # Format: "N/period" where period is second|minute|hour|day
    # These feed directly into slowapi @limiter.limit() decorators.
    rate_limit_login: str = "10/minute"
    rate_limit_register: str = "5/minute"
    rate_limit_forgot_password: str = "5/minute"
    rate_limit_resend_verification: str = "3/minute"
    rate_limit_refresh: str = "30/minute"

    # â”€â”€ CORS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    cors_origins: str | list[str] = "*"
    auto_create_tables: bool = True

    # â”€â”€ Internal / Ops â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    internal_api_key: str = ""

    # â”€â”€ Commercial MEDORAX ERP licensing â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    license_issuer_url: str = ""
    # ERP runtime clients do not receive the issuer administration token.
    # License issuance/revocation remains restricted to the onboarding control plane.
    license_issuer_token: str = ""
    license_public_key_file: str = "/run/secrets/medorax-license/public.pem"
    license_offline_grace_hours: int = 24
    erp_provision_token: str = ""
    # Central Admin ERP customization sync. The ERP authenticates using the installed license envelope.
    admin_sync_url: str = ""
    admin_sync_timeout_seconds: int = 10

    # â”€â”€ Background Tasks (Celery) & Redis â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    redis_url: str = "redis://localhost:6379/0"
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/1"

    # â”€â”€ Object Storage (S3 / MinIO) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    storage_endpoint: str = ""
    storage_access_key: str = ""
    storage_secret_key: str = ""
    storage_secure: bool = False
    storage_bucket_prescriptions: str = "prescriptions"
    storage_bucket_documents: str = "documents"

    # â”€â”€ AI / ML / Search (Optional) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    elasticsearch_url: str | None = None
    llm_api_key: str | None = None
    llm_base_url: str | None = None
    llm_model: str = "qwen-plus"

    # â”€â”€ Validators â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    @model_validator(mode="after")
    def validate_production_secrets(self) -> "Settings":
        """
        Enforce minimum security requirements for production-sensitive values.
        Prevents accidental deployment with weak or default secrets.
        """
        # Block deployment with the known-bad development secret.
        _known_bad = {"CHANGE_ME_DEV_ONLY_SECRET", "secret", "changeme", ""}
        if self.jwt_secret in _known_bad:
            raise ValueError(
                "JWT_SECRET is set to an insecure default. "
                "Generate one with: python -c \"import secrets; print(secrets.token_urlsafe(32))\""
            )
        if len(self.jwt_secret) < 32:
            raise ValueError(
                f"JWT_SECRET must be at least 32 characters. Got {len(self.jwt_secret)}."
            )

        if self.app_env == "production":
            if self.cors_origins == "*" or self.cors_origins == ["*"]:
                raise ValueError("CORS_ORIGINS must explicitly list production frontend origins")
            if not self.database_url:
                raise ValueError("DATABASE_URL is required in production")
            if not self.storage_endpoint or not self.storage_access_key or not self.storage_secret_key:
                raise ValueError("STORAGE_ENDPOINT, STORAGE_ACCESS_KEY and STORAGE_SECRET_KEY are required in production")
            if not self.license_issuer_url:
                raise ValueError("LICENSE_ISSUER_URL is required in production")
            if not self.app_base_url or not self.app_base_url.startswith("https://"):
                raise ValueError("APP_BASE_URL must be an HTTPS URL in production")
            if not self.erp_provision_token:
                raise ValueError("ERP_PROVISION_TOKEN is required in production")
            if self.email_provider == "console":
                raise ValueError("EMAIL_PROVIDER=console is not allowed in production")

        # Warn when non-console email provider is configured without credentials.
        if self.email_provider == "smtp" and not self.smtp_host:
            raise ValueError("SMTP_HOST must be set when EMAIL_PROVIDER=smtp")
        if self.email_provider == "resend" and not self.resend_api_key:
            raise ValueError("RESEND_API_KEY must be set when EMAIL_PROVIDER=resend")

        return self

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
