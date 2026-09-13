"""
app/core/security.py

Password hashing (Argon2id) and JWT helpers.

Refresh token design (ADR-001-D):
  The refresh token is a JWT containing:
    sub  — user UUID
    sid  — session UUID (for O(1) DB routing — avoids a table scan)
    jti  — cryptographically random opaque value (the actual secret)
    type — "refresh"

  Only SHA-256(jti) is stored in Session.refresh_token_hash.
  The full JWT is never stored server-side.

  Why jti-based hashing instead of hashing the full JWT:
    - The JWT header/payload are not secret (base64-encoded).
    - The jti is the only truly random, server-unguessable component.
    - Hashing only the jti makes the stored value independent of
      algorithm or claim changes.
    - The sid in the JWT allows the server to locate the session in
      O(1) without scanning all sessions by token hash alone.

Library choice: PyJWT (not python-jose).
  python-jose had known ECDSA vulnerabilities (CVE-2024-33664 and others).
  PyJWT is actively maintained, has no outstanding CVEs, and is the
  recommended JWT library for Python.
"""

import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from app.core.config import settings

_hasher = PasswordHasher()


def hash_password(plain_password: str) -> str:
    return _hasher.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return _hasher.verify(hashed_password, plain_password)
    except VerifyMismatchError:
        return False


def hash_token(raw_token: str) -> str:
    """Return the SHA-256 hex digest of a raw token string."""
    return hashlib.sha256(raw_token.encode()).hexdigest()


def _create_token(
    subject: str,
    expires_delta: timedelta,
    token_type: str,
    extra_claims: dict | None = None,
) -> str:
    now = datetime.now(timezone.utc)
    payload: dict[str, Any] = {
        "sub": subject,
        "type": token_type,
        "iat": int(now.timestamp()),
        "exp": int((now + expires_delta).timestamp()),
    }
    if extra_claims:
        payload.update(extra_claims)
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def create_access_token(user_id: str, session_id: str) -> str:
    """
    Issue a signed JWT access token (stateless, short-lived).

    Claims:
      sub  — user UUID (string)
      sid  — session UUID; used for stateful validation on each request
      type — "access"; prevents a refresh token being used as an access token
      iat  — issued-at timestamp (unix int, used for password_updated_at check)
      exp  — expiry timestamp
    """
    return _create_token(
        subject=user_id,
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
        token_type="access",
        extra_claims={"sid": session_id},
    )


def create_refresh_token(user_id: str, session_id: str) -> tuple[str, str]:
    """
    Issue a refresh token and return (signed_jwt, jti_hash).

    The jti is a cryptographically random opaque value — the actual secret.
    Only SHA-256(jti) is stored in Session.refresh_token_hash.
    The full JWT is never stored server-side.

    Returns:
        (signed_jwt, jti_hash) — caller stores jti_hash, sends signed_jwt to client.
    """
    jti = secrets.token_urlsafe(32)  # The actual secret — random, never stored
    jti_hash = hash_token(jti)       # Only this hash is stored in the DB

    signed_token = _create_token(
        subject=user_id,
        expires_delta=timedelta(days=settings.refresh_token_expire_days),
        token_type="refresh",
        extra_claims={"sid": session_id, "jti": jti},
    )
    return signed_token, jti_hash


def decode_token(token: str) -> dict:
    """
    Decode and verify a JWT.
    Raises jwt.PyJWTError (and subclasses) if invalid, expired, or tampered.
    """
    return jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[settings.jwt_algorithm],
    )
