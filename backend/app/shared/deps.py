"""
app/shared/deps.py

FastAPI dependency for authenticated requests.

Per-request validation (one SELECT with joinedload — 1 DB query):
  1. Decode and verify JWT signature + expiry.
  2. Verify token type is "access" (prevents refresh token misuse).
  3. Load Session + Device in a single JOIN query.
  4. Assert session is not revoked.
  5. Assert session has not expired.
  6. Assert device is still active.
  7. Load User and assert account is active.
  8. Assert access token was issued AFTER the user's last password change.
     This ensures tokens issued before a password reset are invalidated
     immediately, without waiting for their natural 15-minute expiry.
"""

from datetime import datetime, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session as DbSession, joinedload

from app.auth.models import Session as AuthSession
from app.core.config import settings
from app.core.security import decode_token
from app.db.base import get_db
from app.user.models import User


def _utcnow() -> datetime:
    """Return timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)


bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: DbSession = Depends(get_db),
) -> User:
    """
    Validate the bearer token and return the authenticated User.

    Raises HTTP 401 on any validation failure.
    Attaches `_current_session_id` to the User object so routes (e.g. logout)
    can reference it without re-decoding the token.
    """
    token = credentials.credentials

    try:
        payload = decode_token(token)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong token type",
        )

    session_id = payload.get("sid")
    user_id = payload.get("sub")
    token_iat = payload.get("iat")  # Issued-at claim (unix int)

    if not session_id or not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Malformed token payload",
        )

    # Single JOIN query: session + device in one DB round-trip.
    session = (
        db.query(AuthSession)
        .options(joinedload(AuthSession.device))
        .filter(AuthSession.id == session_id)
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session not found",
        )

    if session.revoked:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session has been revoked",
        )

    if session.expires_at < _utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session has expired",
        )

    # Assert the device is still active.
    if session.device and not session.device.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Device is deactivated",
        )

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is inactive",
        )

    # Invalidate tokens issued before the user's last password change.
    # This handles the case where a token is stolen and the user resets
    # their password — the stolen token is rejected immediately even if
    # it has not yet expired (OWASP ASVS V2.2.7 / ADR-001-C).
    if token_iat is not None and user.password_updated_at is not None:
        password_changed_ts = int(user.password_updated_at.timestamp())
        if token_iat < password_changed_ts:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalidated by password change — please log in again",
            )

    # Stash session id so routes (e.g. logout) can use it without re-decoding.
    user._current_session_id = session_id  # type: ignore[attr-defined]
    return user
