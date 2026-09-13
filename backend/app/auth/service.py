"""
app/auth/service.py

Service layer for authentication, device management, and session lifecycle.

Design rules (ADR-001):
  - Business logic lives here, never in routers or models.
  - Routers call services. Services call the ORM. Models stay thin.
  - Every session revocation goes through revoke_sessions() so that
    revoked_at and logout_reason are always set consistently.
  - Refresh tokens are JWTs with a random jti claim.
    Only SHA-256(jti) is stored. Plaintext never persisted.
  - One active session per device. Re-login on the same device revokes
    the prior session (logout_reason='session_replaced').

Email delivery:
  - Services return raw tokens to callers. They do NOT send emails.
  - The router layer calls email_service.send_*() via BackgroundTasks.
  - This keeps FastAPI lifecycle objects (BackgroundTasks, Request) in
    the router where they belong, and keeps services pure Python.
"""

import logging
import secrets
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, status
from sqlalchemy.orm import Session as DbSession, joinedload

from app.auth.models import (
    Credential,
    Device,
    EmailVerificationToken,
    LoginHistory,
    PasswordResetToken,
)
from app.auth.models import Session as AuthSession
from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    hash_token,
    verify_password,
)
from app.services.audit import audit_log
from app.user.models import User
from app.user.service import get_user_by_email, get_user_by_phone, get_user_by_username

logger = logging.getLogger("medorax.auth")

# Pre-computed dummy Argon2 hash evaluated on every failed login attempt
# where the user identifier does not exist. Without this, response timing
# would reveal whether a given email/phone is registered (OWASP ASVS V2.2.2).
_DUMMY_HASH = hash_password("dummy_password_for_timing_protection_DO_NOT_USE")


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _utcnow() -> datetime:
    """Return timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)


def _get_user_by_identifier(db: DbSession, identifier: str) -> User | None:
    """Resolve a User by email or phone number."""
    if "@" in identifier:
        return get_user_by_email(db, identifier)
    user = get_user_by_username(db, identifier.strip().lower())
    if user:
        return user
    return get_user_by_phone(db, identifier)


def _parse_user_agent(user_agent: str | None) -> tuple[str | None, str | None]:
    """
    Derive browser and operating_system from a raw User-Agent string.
    Returns (browser, operating_system). Both may be None.

    Intentionally simple. A full UA parser library (ua-parser) can replace
    this without changing the calling interface.
    """
    if not user_agent:
        return None, None

    ua = user_agent.lower()

    if "firefox" in ua:
        browser = "Firefox"
    elif "edg" in ua:
        browser = "Edge"
    elif "chrome" in ua:
        browser = "Chrome"
    elif "safari" in ua:
        browser = "Safari"
    else:
        browser = None

    if "android" in ua:
        os_name = "Android"
    elif "iphone" in ua or "ipad" in ua:
        os_name = "iOS"
    elif "win" in ua:
        os_name = "Windows"
    elif "mac" in ua:
        os_name = "macOS"
    elif "linux" in ua:
        os_name = "Linux"
    else:
        os_name = None

    return browser, os_name


def revoke_sessions(
    db: DbSession,
    query,
    logout_reason: str,
) -> int:
    """
    Central revocation helper. ALL session revocations in this codebase
    must go through this function so that revoked_at and logout_reason
    are always populated consistently.

    Returns the count of sessions revoked.
    """
    now = _utcnow()
    result = (
        query
        .filter(AuthSession.revoked.is_(False))
        .update(
            {"revoked": True, "revoked_at": now, "logout_reason": logout_reason},
            synchronize_session=False,
        )
    )
    return result


def _record_login_attempt(
    db: DbSession,
    *,
    user_id: str | None,
    session_id: str | None,
    device_id: str | None,
    success: bool,
    ip: str | None,
    ua: str | None,
) -> None:
    """Append an immutable record to the login audit log."""
    db.add(LoginHistory(
        user_id=user_id,
        session_id=session_id,
        device_id=device_id,
        success=success,
        ip_address=ip,
        user_agent=ua,
    ))
    db.flush()
    if not success:
        db.commit()


# ---------------------------------------------------------------------------
# Registration & Email Verification
# ---------------------------------------------------------------------------

def register_user(
    db: DbSession,
    name: str,
    email: str | None,
    phone: str | None,
    password: str,
) -> tuple[User, str | None]:
    """
    Create a new user account and generate an email verification token.

    Returns:
        (user, raw_verification_token) — the router passes raw_token to
        email_service.send_verification_email() via BackgroundTasks.
        raw_token is None if no email address was provided.
    """
    if settings.email_required and not email:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email is required")
    if settings.phone_required and not phone:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Phone is required")

    if email and get_user_by_email(db, email):
        raise HTTPException(status.HTTP_409_CONFLICT, "Email already registered")
    if phone and get_user_by_phone(db, phone):
        raise HTTPException(status.HTTP_409_CONFLICT, "Phone already registered")

    try:
        user = User(
            name=name,
            email=email,
            phone=phone,
            email_verified=False,
            phone_verified=False,
        )
        db.add(user)
        db.flush()

        credential = Credential(user_id=user.id, password_hash=hash_password(password))
        db.add(credential)

        raw_token: str | None = None
        if email:
            raw_token = secrets.token_urlsafe(32)
            db.add(EmailVerificationToken(
                user_id=user.id,
                token_hash=hash_token(raw_token),
                expires_at=_utcnow() + timedelta(hours=settings.cleanup_verification_token_hours),
            ))

        db.commit()
        db.refresh(user)

        audit_log("USER_REGISTERED", user_id=user.id, email=email, has_phone=bool(phone))
        return user, raw_token

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Registration failed: {e}") from e


def verify_email_token(db: DbSession, raw_token: str) -> bool:
    token_hash = hash_token(raw_token)
    record = (
        db.query(EmailVerificationToken)
        .options(joinedload(EmailVerificationToken.user))
        .filter(EmailVerificationToken.token_hash == token_hash)
        .first()
    )

    if not record:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid or expired token")

    if not secrets.compare_digest(record.token_hash, token_hash):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid or expired token")

    if record.used:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Token already used")

    if record.expires_at < _utcnow():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Token expired")

    try:
        record.used = True
        record.user.email_verified = True
        db.commit()
        audit_log("EMAIL_VERIFIED", user_id=record.user_id)
        return True
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, f"Email verification failed: {e}"
        ) from e


def resend_verification_email(db: DbSession, email: str) -> str | None:
    """
    Generate a new verification token.

    Always returns None (for the HTTP response) regardless of whether the
    email exists or is already verified — prevents email enumeration (OWASP ASVS V2.6.2).

    Returns the raw token to the router so it can send the email via BackgroundTasks.
    If there is nothing to send (unknown user, already verified), returns None.
    """
    user = get_user_by_email(db, email)
    if not user or user.email_verified:
        return None

    try:
        db.query(EmailVerificationToken).filter(
            EmailVerificationToken.user_id == user.id,
            EmailVerificationToken.used.is_(False),
        ).update({"expires_at": _utcnow()}, synchronize_session=False)

        raw_token = secrets.token_urlsafe(32)
        db.add(EmailVerificationToken(
            user_id=user.id,
            token_hash=hash_token(raw_token),
            expires_at=_utcnow() + timedelta(hours=settings.cleanup_verification_token_hours),
        ))
        db.commit()
        return raw_token
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, f"Failed to resend token: {e}"
        ) from e


# ---------------------------------------------------------------------------
# Password Reset
# ---------------------------------------------------------------------------

def forgot_password(db: DbSession, identifier: str) -> str | None:
    """
    Generate a password reset token for the given identifier.

    Always returns without error regardless of whether the identifier exists —
    prevents user enumeration (OWASP ASVS V2.6.2).

    Returns the raw token to the router so it can send the email via BackgroundTasks.
    Returns None if identifier not found (router still returns 200).
    """
    user = _get_user_by_identifier(db, identifier)
    if not user:
        return None

    try:
        db.query(PasswordResetToken).filter(
            PasswordResetToken.user_id == user.id,
            PasswordResetToken.used.is_(False),
        ).update({"expires_at": _utcnow()}, synchronize_session=False)

        raw_token = secrets.token_urlsafe(32)
        db.add(PasswordResetToken(
            user_id=user.id,
            token_hash=hash_token(raw_token),
            expires_at=_utcnow() + timedelta(hours=settings.cleanup_password_reset_token_hours),
        ))
        db.commit()

        audit_log("PASSWORD_RESET_REQUESTED", user_id=user.id)
        return raw_token
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, f"Forgot password request failed: {e}"
        ) from e


def reset_password(db: DbSession, raw_token: str, new_password: str) -> None:
    token_hash = hash_token(raw_token)
    record = (
        db.query(PasswordResetToken)
        .options(joinedload(PasswordResetToken.user))
        .filter(PasswordResetToken.token_hash == token_hash)
        .first()
    )

    if not record:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid or expired token")

    if not secrets.compare_digest(record.token_hash, token_hash):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid or expired token")

    if record.used:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Token already used")

    if record.expires_at < _utcnow():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Token expired")

    try:
        record.used = True
        user = record.user
        credential = db.query(Credential).filter(Credential.user_id == user.id).first()
        if not credential:
            credential = Credential(user_id=user.id)
            db.add(credential)
        credential.password_hash = hash_password(new_password)
        user.password_updated_at = _utcnow()

        revoke_sessions(
            db,
            db.query(AuthSession).filter(AuthSession.user_id == user.id),
            logout_reason="password_reset",
        )

        db.commit()
        audit_log("PASSWORD_RESET_COMPLETED", user_id=user.id)
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, f"Password reset failed: {e}"
        ) from e


# ---------------------------------------------------------------------------
# Authentication & Session Lifecycle
# ---------------------------------------------------------------------------

def authenticate(
    db: DbSession,
    identifier: str,
    password: str,
    device_identifier: str | None = None,
    device_name: str | None = None,
    platform: str | None = "web",
    app_version: str | None = None,
    push_token: str | None = None,
    ip_address: str | None = None,
    user_agent: str | None = None,
) -> tuple[str, str, str]:
    """
    Authenticate a user and issue a token pair.

    Returns (access_token, refresh_token, device_identifier_str).

    Device lifecycle (ADR-001-A):
      - device_identifier identifies a client installation, not hardware.
      - If no device_identifier is supplied, one is generated server-side.
        The client MUST persist and return the value in the response.
      - Existing device: telemetry is updated.
      - New device: a new Device row is created.

    Session policy (ADR-001-B):
      - Any existing active session for this (user, device) pair is revoked
        before creating a new one (logout_reason='session_replaced').
    """
    user = _get_user_by_identifier(db, identifier)

    if not user:
        _record_login_attempt(
            db, user_id=None, session_id=None, device_id=None,
            success=False, ip=ip_address, ua=user_agent,
        )
        verify_password(password, _DUMMY_HASH)
        audit_log("LOGIN_FAILED", reason="user_not_found", ip_address=ip_address)
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")

    credential = db.query(Credential).filter(Credential.user_id == user.id).first()
    if not credential or not verify_password(password, credential.password_hash):
        _record_login_attempt(
            db, user_id=user.id, session_id=None, device_id=None,
            success=False, ip=ip_address, ua=user_agent,
        )
        audit_log("LOGIN_FAILED", user_id=user.id, reason="bad_password", ip_address=ip_address)
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")

    if not user.is_active:
        audit_log("LOGIN_FAILED", user_id=user.id, reason="account_disabled", ip_address=ip_address)
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Account is disabled")

    if settings.email_required and not user.email_verified:
        audit_log("LOGIN_FAILED", user_id=user.id, reason="email_not_verified", ip_address=ip_address)
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Email verification required before login")

    if settings.require_phone_verification_for_login and not user.phone_verified:
        if "@" not in identifier:
            audit_log("LOGIN_FAILED", user_id=user.id, reason="phone_not_verified", ip_address=ip_address)
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Phone verification required")

    # ERP authentication is gated by the commercial tenant license. The first
    # successful login automatically activates this client against the
    # provisioned license; later logins revalidate the activation.
    browser, os_name = _parse_user_agent(user_agent)
    if not device_identifier:
        import uuid
        device_identifier = str(uuid.uuid4())
    from app.licensing.service import ensure_login_license
    ensure_login_license(
        db, user, device_identifier,
        device_name or f"{browser or 'Browser'} on {os_name or 'Unknown'}",
    )

    try:
        device = (
            db.query(Device)
            .filter(Device.user_id == user.id, Device.device_identifier == device_identifier)
            .first()
        )

        is_new_device = device is None
        if device:
            device.browser = browser
            device.operating_system = os_name
            device.user_agent = user_agent
            if device_name:
                device.device_name = device_name
            if push_token:
                device.push_token = push_token
            if app_version:
                device.app_version = app_version

            reactivated = not device.is_active
            if not device.is_active:
                device.is_active = True
                audit_log("DEVICE_REACTIVATED", user_id=user.id, device_id=device.id)

            db.flush()
        else:
            device = Device(
                user_id=user.id,
                device_identifier=device_identifier,
                platform=platform or "web",
                device_name=device_name or f"{browser or 'Unknown'} on {os_name or 'Unknown'}",
                browser=browser,
                operating_system=os_name,
                app_version=app_version,
                user_agent=user_agent,
                push_token=push_token,
                trusted=False,
                is_active=True,
            )
            db.add(device)
            db.flush()
            audit_log("DEVICE_ADDED", user_id=user.id, device_id=device.id,
                      platform=platform, ip_address=ip_address)

        # One-session-per-device policy (ADR-001-B)
        replaced_count = revoke_sessions(
            db,
            db.query(AuthSession).filter(AuthSession.device_id == device.id),
            logout_reason="session_replaced",
        )
        if replaced_count:
            audit_log("SESSION_REPLACED", user_id=user.id, device_id=device.id,
                      count=replaced_count)

        # Global session limit (ADR-001-C)
        if settings.max_active_devices is not None:
            active_sessions = (
                db.query(AuthSession.id)
                .filter(AuthSession.user_id == user.id, AuthSession.revoked.is_(False))
                .order_by(AuthSession.created_at.asc())
                .all()
            )
            overflow = len(active_sessions) - settings.max_active_devices + 1
            if overflow > 0:
                ids_to_revoke = [row.id for row in active_sessions[:overflow]]
                revoke_sessions(
                    db,
                    db.query(AuthSession).filter(AuthSession.id.in_(ids_to_revoke)),
                    logout_reason="limit_enforced",
                )

        # Issue tokens
        now = _utcnow()
        session = AuthSession(
            user_id=user.id,
            device_id=device.id,
            refresh_token_hash="placeholder",
            ip_address=ip_address,
            user_agent=user_agent,
            last_activity_at=now,
            expires_at=now + timedelta(days=settings.refresh_token_expire_days),
            revoked=False,
        )
        db.add(session)
        db.flush()

        raw_refresh, jti_hash = create_refresh_token(user_id=user.id, session_id=session.id)
        session.refresh_token_hash = jti_hash
        db.flush()

        access_token = create_access_token(user_id=user.id, session_id=session.id)

        _record_login_attempt(
            db,
            user_id=user.id, session_id=session.id, device_id=device.id,
            success=True, ip=ip_address, ua=user_agent,
        )

        db.commit()
        audit_log("LOGIN_SUCCESS", user_id=user.id, session_id=session.id,
                  device_id=device.id, ip_address=ip_address, is_new_device=is_new_device)
        return access_token, raw_refresh, str(device_identifier)

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, f"Login failed: {e}"
        ) from e


def refresh_access_token(db: DbSession, refresh_token: str) -> tuple[str, str]:
    """
    Rotate the refresh token (RTR).

    Rotation breach detection (ADR Security Model):
      If the JWT signature is valid but SHA-256(jti) does NOT match the
      stored hash, the token was already rotated. This is a replay attack.
      All of the user's sessions are immediately revoked.
    """
    try:
        payload = jwt.decode(
            refresh_token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
    except jwt.PyJWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or expired refresh token")

    if payload.get("type") != "refresh":
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Wrong token type")

    session_id = payload.get("sid")
    user_id = payload.get("sub")
    jti = payload.get("jti")

    if not session_id or not user_id or not jti:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Malformed token payload")

    session = (
        db.query(AuthSession)
        .options(joinedload(AuthSession.user), joinedload(AuthSession.device))
        .filter(AuthSession.id == session_id)
        .first()
    )

    incoming_jti_hash = hash_token(jti)

    # Rotation breach detection
    if (
        session
        and not session.revoked
        and session.expires_at >= _utcnow()
    ):
        if not secrets.compare_digest(session.refresh_token_hash, incoming_jti_hash):
            logger.warning(
                "ROTATION_BREACH_DETECTED user=%s session=%s — revoking all sessions",
                user_id, session_id,
            )
            audit_log("ROTATION_BREACH", user_id=user_id, session_id=session_id)
            revoke_sessions(
                db,
                db.query(AuthSession).filter(AuthSession.user_id == user_id),
                logout_reason="rotation_breach",
            )
            db.commit()
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                "Session invalidated due to security event",
            )

    if not session or session.revoked or session.expires_at < _utcnow():
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Session is no longer valid")

    if not session.device or not session.device.is_active:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Device is deactivated")

    try:
        now = _utcnow()
        new_raw_refresh, new_jti_hash = create_refresh_token(
            user_id=str(session.user_id), session_id=str(session.id)
        )
        session.refresh_token_hash = new_jti_hash
        session.last_activity_at = now
        session.expires_at = now + timedelta(days=settings.refresh_token_expire_days)
        db.flush()

        new_access_token = create_access_token(
            user_id=str(session.user_id), session_id=str(session.id)
        )

        db.commit()
        audit_log("TOKEN_ROTATED", user_id=str(session.user_id), session_id=str(session.id))
        return new_access_token, new_raw_refresh
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, f"Token refresh failed: {e}"
        ) from e


# ---------------------------------------------------------------------------
# Logout
# ---------------------------------------------------------------------------

def logout(db: DbSession, session_id: str) -> None:
    """Revoke a specific session (standard user logout)."""
    revoke_sessions(
        db,
        db.query(AuthSession).filter(AuthSession.id == session_id),
        logout_reason="user_logout",
    )
    db.commit()
    audit_log("SESSION_REVOKED", session_id=session_id, reason="user_logout")


def logout_all(db: DbSession, user_id: str, exclude_session_id: str | None = None) -> None:
    """Revoke all of a user's active sessions."""
    query = db.query(AuthSession).filter(AuthSession.user_id == user_id)
    if exclude_session_id:
        query = query.filter(AuthSession.id != exclude_session_id)
    count = revoke_sessions(db, query, logout_reason="logout_all")
    db.commit()
    audit_log("SESSION_REVOKED", user_id=user_id, reason="logout_all", count=count)


# ---------------------------------------------------------------------------
# Session queries & management
# ---------------------------------------------------------------------------

def get_user_sessions(db: DbSession, user_id: str) -> list[AuthSession]:
    return (
        db.query(AuthSession)
        .options(joinedload(AuthSession.device))
        .filter(
            AuthSession.user_id == user_id,
            AuthSession.revoked.is_(False),
            AuthSession.expires_at > _utcnow(),
        )
        .order_by(AuthSession.last_activity_at.desc())
        .all()
    )


def revoke_session(db: DbSession, user_id: str, session_id: str) -> None:
    session = db.query(AuthSession).filter(
        AuthSession.id == session_id,
        AuthSession.user_id == user_id,
    ).first()
    if not session:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Session not found")
    revoke_sessions(
        db,
        db.query(AuthSession).filter(AuthSession.id == session_id),
        logout_reason="user_logout",
    )
    db.commit()
    audit_log("SESSION_REVOKED", user_id=user_id, session_id=session_id, reason="user_logout")


# ---------------------------------------------------------------------------
# Device Management
# ---------------------------------------------------------------------------

def get_user_devices(db: DbSession, user_id: str) -> list[Device]:
    return (
        db.query(Device)
        .filter(Device.user_id == user_id, Device.is_active.is_(True))
        .order_by(Device.last_seen_at.desc())
        .all()
    )


def get_device_by_id(db: DbSession, user_id: str, device_id: str) -> Device:
    device = db.query(Device).filter(
        Device.id == device_id,
        Device.user_id == user_id,
        Device.is_active.is_(True),
    ).first()
    if not device:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Device not found")
    return device


def update_device(
    db: DbSession,
    user_id: str,
    device_id: str,
    friendly_name: str | None,
    trusted: bool | None,
) -> Device:
    device = get_device_by_id(db, user_id, device_id)
    if friendly_name is not None:
        device.friendly_name = friendly_name
    if trusted is not None:
        device.trusted = trusted
    db.commit()
    db.refresh(device)
    return device


def deactivate_device(db: DbSession, user_id: str, device_id: str) -> None:
    """
    Soft-deactivate a device and revoke all its active sessions.
    The device record is retained for audit history.
    """
    device = db.query(Device).filter(
        Device.id == device_id,
        Device.user_id == user_id,
        Device.is_active.is_(True),
    ).first()
    if not device:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Device not found")

    try:
        device.is_active = False
        db.flush()

        revoke_sessions(
            db,
            db.query(AuthSession).filter(AuthSession.device_id == device_id),
            logout_reason="device_deactivated",
        )
        db.commit()
        audit_log("DEVICE_DEACTIVATED", user_id=user_id, device_id=device_id)
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, f"Device deactivation failed: {e}"
        ) from e
