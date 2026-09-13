"""
app/services/email_service.py

Email delivery for transactional emails (verification, password reset).

Provider selection:
  EMAIL_PROVIDER=console  — logs to stdout (development / CI)
  EMAIL_PROVIDER=smtp     — sends via SMTP (self-hosted, Gmail, etc.)
  EMAIL_PROVIDER=resend   — sends via Resend HTTP API (https://resend.com)

Design principles:
  - All provider logic is in one file. If you need to add SendGrid, add an
    `elif` branch. No class hierarchy needed for a single hot-swap point.
  - All providers catch their own exceptions and re-raise as EmailSendError.
    The caller (router layer, via BackgroundTasks) catches EmailSendError,
    logs it, and does NOT propagate it to the HTTP response.
  - Email sends are always fire-and-forget from the user's perspective.
    A failed email does not fail the registration or password reset flow.
  - Tokens are embedded as query parameters so the client app can deep-link
    to the appropriate screen. Template is plain HTML — no Jinja2 dependency.

Upgrade path:
  - For retries: wrap send_email() calls in a Celery/Dramatiq task.
    The function signature does not change.
  - For Redis-backed rate limiting of email sends: add a check before sending.
  - For HTML templates: replace the f-string bodies with jinja2.Template.render().

New dependencies introduced: httpx (Resend provider).
  httpx is a transitive dependency of starlette/fastapi in most installations.
  It is explicitly pinned in requirements.txt.
"""

import logging
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings

logger = logging.getLogger("medorax.email")


class EmailSendError(Exception):
    """Raised when email delivery fails after all provider-level retries."""


# ---------------------------------------------------------------------------
# Email templates
# ---------------------------------------------------------------------------

def _verification_email_html(verification_url: str) -> str:
    return f"""
    <html><body>
      <h2>Verify your Medorax account</h2>
      <p>Click the link below to verify your email address.
         This link expires in {settings.cleanup_verification_token_hours} hours.</p>
      <p><a href="{verification_url}" style="
            display:inline-block;padding:12px 24px;
            background:#2563eb;color:#fff;
            border-radius:6px;text-decoration:none;font-weight:bold;">
        Verify Email
      </a></p>
      <p>Or copy this link:<br><code>{verification_url}</code></p>
      <p>If you did not create a Medorax account, ignore this email.</p>
    </body></html>
    """


def _password_reset_email_html(reset_url: str) -> str:
    return f"""
    <html><body>
      <h2>Reset your Medorax password</h2>
      <p>Click the link below to reset your password.
         This link expires in {settings.cleanup_password_reset_token_hours} hours.</p>
      <p><a href="{reset_url}" style="
            display:inline-block;padding:12px 24px;
            background:#dc2626;color:#fff;
            border-radius:6px;text-decoration:none;font-weight:bold;">
        Reset Password
      </a></p>
      <p>Or copy this link:<br><code>{reset_url}</code></p>
      <p>If you did not request a password reset, ignore this email.
         Your password has NOT been changed.</p>
    </body></html>
    """


# ---------------------------------------------------------------------------
# Core send function — provider dispatch
# ---------------------------------------------------------------------------

def send_email(to: str, subject: str, html_body: str) -> None:
    """
    Deliver an email synchronously.

    Raises EmailSendError on any delivery failure.
    Callers that want fire-and-forget should use background_tasks.add_task(send_email, ...)
    and wrap in a try/except at the background task level.
    """
    provider = settings.email_provider.lower()

    try:
        if provider == "smtp":
            _send_smtp(to, subject, html_body)
        elif provider == "resend":
            _send_resend(to, subject, html_body)
        else:
            # "console" provider — development / CI / test mode.
            # Logs the email content. Tokens are visible in server stdout.
            logger.info(
                "EMAIL_CONSOLE_DELIVERY to=%s subject=%s "
                "(set EMAIL_PROVIDER=smtp or resend for real delivery)",
                to, subject,
            )
            # Print the full body in debug mode for local token extraction.
            logger.debug("EMAIL_BODY to=%s\n%s", to, html_body)

    except EmailSendError:
        raise
    except Exception as exc:
        # Normalise provider-specific exceptions to EmailSendError so callers
        # have a single exception type to handle.
        raise EmailSendError(f"[{provider}] Failed to send to {to}: {exc}") from exc


def _send_smtp(to: str, subject: str, html_body: str) -> None:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{settings.email_from_name} <{settings.email_from}>"
    msg["To"] = to
    msg.attach(MIMEText(html_body, "html"))

    context = ssl.create_default_context() if settings.smtp_use_tls else None

    try:
        if settings.smtp_use_tls:
            with smtplib.SMTP(
                settings.smtp_host,
                settings.smtp_port,
                timeout=settings.smtp_timeout_seconds,
            ) as server:
                server.ehlo()
                server.starttls(context=context)
                if settings.smtp_user:
                    server.login(settings.smtp_user, settings.smtp_password)
                server.sendmail(settings.email_from, [to], msg.as_string())
        else:
            with smtplib.SMTP(
                settings.smtp_host,
                settings.smtp_port,
                timeout=settings.smtp_timeout_seconds,
            ) as server:
                if settings.smtp_user:
                    server.login(settings.smtp_user, settings.smtp_password)
                server.sendmail(settings.email_from, [to], msg.as_string())
    except (smtplib.SMTPConnectError, smtplib.SMTPServerDisconnected) as exc:
        raise EmailSendError(f"SMTP server unavailable: {exc}") from exc
    except smtplib.SMTPAuthenticationError as exc:
        raise EmailSendError(f"SMTP authentication failed: {exc}") from exc
    except smtplib.SMTPException as exc:
        raise EmailSendError(f"SMTP send failed: {exc}") from exc
    except TimeoutError as exc:
        raise EmailSendError(f"SMTP connection timed out: {exc}") from exc


def _send_resend(to: str, subject: str, html_body: str) -> None:
    try:
        import httpx
    except ImportError:
        raise EmailSendError(
            "httpx is required for the Resend email provider. "
            "Add 'httpx' to requirements.txt."
        )

    payload = {
        "from": f"{settings.email_from_name} <{settings.email_from}>",
        "to": [to],
        "subject": subject,
        "html": html_body,
    }
    try:
        response = httpx.post(
            "https://api.resend.com/emails",
            json=payload,
            headers={"Authorization": f"Bearer {settings.resend_api_key}"},
            timeout=settings.resend_timeout_seconds,
        )
        if response.status_code == 429:
            raise EmailSendError(
                f"Resend rate limit exceeded (429). Retry after: "
                f"{response.headers.get('Retry-After', 'unknown')}s"
            )
        if response.status_code >= 400:
            raise EmailSendError(
                f"Resend API error {response.status_code}: {response.text}"
            )
    except httpx.TimeoutException as exc:
        raise EmailSendError(f"Resend API timeout: {exc}") from exc
    except httpx.RequestError as exc:
        raise EmailSendError(f"Resend network error: {exc}") from exc


# ---------------------------------------------------------------------------
# High-level email senders — called from router via BackgroundTasks
# ---------------------------------------------------------------------------

def send_verification_email(to: str, raw_token: str) -> None:
    """
    Send the email-verification link to a newly registered user.

    This function is intended to be called via FastAPI BackgroundTasks:
        background_tasks.add_task(send_verification_email, to=user.email, raw_token=token)

    Failures are logged as EMAIL_FAILED audit events and do not propagate
    to the HTTP response.
    """
    from app.services.audit import audit_log  # local import avoids circular dep

    url = f"{settings.app_base_url}/auth/verify-email?token={raw_token}"
    try:
        send_email(
            to=to,
            subject="Verify your Medorax account",
            html_body=_verification_email_html(url),
        )
        audit_log("EMAIL_SENT", email_type="verification", recipient=to)
        logger.info("EMAIL_SENT type=verification to=%s", to)
    except EmailSendError as exc:
        audit_log("EMAIL_FAILED", email_type="verification", recipient=to, error=str(exc))
        logger.error("EMAIL_FAILED type=verification to=%s error=%s", to, exc)
        # Do not re-raise — background task failure must not crash the worker.


def send_password_reset_email(to: str, raw_token: str) -> None:
    """
    Send the password-reset link.

    Intended to be called via FastAPI BackgroundTasks.
    Failures are logged and do not propagate.
    """
    from app.services.audit import audit_log

    url = f"{settings.app_base_url}/auth/reset-password?token={raw_token}"
    try:
        send_email(
            to=to,
            subject="Reset your Medorax password",
            html_body=_password_reset_email_html(url),
        )
        audit_log("EMAIL_SENT", email_type="password_reset", recipient=to)
        logger.info("EMAIL_SENT type=password_reset to=%s", to)
    except EmailSendError as exc:
        audit_log("EMAIL_FAILED", email_type="password_reset", recipient=to, error=str(exc))
        logger.error("EMAIL_FAILED type=password_reset to=%s error=%s", to, exc)
