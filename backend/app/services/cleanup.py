"""
app/services/cleanup.py

Database cleanup functions for expired / stale records.

Design:
  - Each function is self-contained: it opens no sessions, makes no HTTP
    calls, and has no side effects beyond its one DELETE (or UPDATE) query.
  - All functions accept a db session and return a count of deleted rows.
  - The orchestrator `run_all_cleanup()` calls all five functions and returns
    a summary dict. This is what the /internal/cleanup endpoint calls.
  - None of these functions delete active users or active sessions.

Deployment:
  - These functions are exposed via POST /internal/cleanup (protected by
    INTERNAL_API_KEY). Run from a system cron job or Kubernetes CronJob:
      0 3 * * *  curl -s -X POST https://api.medorax.com/internal/cleanup \\
                   -H "X-Internal-Key: $INTERNAL_API_KEY"
  - They are NOT run in-process via asyncio.sleep (that causes multi-worker
    race conditions when running Gunicorn with multiple workers).

All retention periods are configurable via Settings.
"""

import logging
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session as DbSession

from app.auth.models import (
    EmailVerificationToken,
    PasswordResetToken,
)
from app.auth.models import Session as AuthSession
from app.core.config import settings
from app.user.models import User

logger = logging.getLogger("medorax.cleanUp")


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def cleanup_expired_verification_tokens(db: DbSession) -> int:
    """
    Delete email_verification_tokens that are either used or past retention in batches.
    """
    cutoff = _utcnow() - timedelta(hours=settings.cleanup_verification_token_hours)
    total_deleted = 0
    while True:
        ids = [
            row[0]
            for row in db.query(EmailVerificationToken.id)
            .filter(
                (EmailVerificationToken.used.is_(True))
                | (EmailVerificationToken.expires_at < cutoff)
            )
            .limit(5000)
            .all()
        ]
        if not ids:
            break
        deleted = (
            db.query(EmailVerificationToken)
            .filter(EmailVerificationToken.id.in_(ids))
            .delete(synchronize_session=False)
        )
        db.commit()
        total_deleted += deleted
    logger.info("CLEANUP expired_verification_tokens deleted=%d", total_deleted)
    return total_deleted


def cleanup_expired_password_reset_tokens(db: DbSession) -> int:
    """
    Delete password_reset_tokens that are either used or past retention in batches.
    """
    cutoff = _utcnow() - timedelta(hours=settings.cleanup_password_reset_token_hours)
    total_deleted = 0
    while True:
        ids = [
            row[0]
            for row in db.query(PasswordResetToken.id)
            .filter(
                (PasswordResetToken.used.is_(True))
                | (PasswordResetToken.expires_at < cutoff)
            )
            .limit(5000)
            .all()
        ]
        if not ids:
            break
        deleted = (
            db.query(PasswordResetToken)
            .filter(PasswordResetToken.id.in_(ids))
            .delete(synchronize_session=False)
        )
        db.commit()
        total_deleted += deleted
    logger.info("CLEANUP expired_password_reset_tokens deleted=%d", total_deleted)
    return total_deleted


def cleanup_revoked_sessions(db: DbSession) -> int:
    """
    Delete sessions that have been revoked AND whose revoked_at is older than retention in batches.
    """
    cutoff = _utcnow() - timedelta(days=settings.cleanup_revoked_session_days)
    total_deleted = 0
    while True:
        ids = [
            row[0]
            for row in db.query(AuthSession.id)
            .filter(
                AuthSession.revoked.is_(True),
                (AuthSession.revoked_at < cutoff)
                | (
                    (AuthSession.revoked_at.is_(None))
                    & (AuthSession.expires_at < cutoff)
                ),
            )
            .limit(5000)
            .all()
        ]
        if not ids:
            break
        deleted = (
            db.query(AuthSession)
            .filter(AuthSession.id.in_(ids))
            .delete(synchronize_session=False)
        )
        db.commit()
        total_deleted += deleted
    logger.info("CLEANUP revoked_sessions deleted=%d", total_deleted)
    return total_deleted


def cleanup_old_login_history(db: DbSession) -> int:
    """
    Delete login_history rows older than retention in batches.
    """
    from app.auth.models import LoginHistory

    cutoff = _utcnow() - timedelta(days=settings.cleanup_login_history_days)
    total_deleted = 0
    while True:
        ids = [
            row[0]
            for row in db.query(LoginHistory.id)
            .filter(LoginHistory.created_at < cutoff)
            .limit(5000)
            .all()
        ]
        if not ids:
            break
        deleted = (
            db.query(LoginHistory)
            .filter(LoginHistory.id.in_(ids))
            .delete(synchronize_session=False)
        )
        db.commit()
        total_deleted += deleted
    logger.info("CLEANUP old_login_history deleted=%d", total_deleted)
    return total_deleted


def cleanup_unverified_users(db: DbSession) -> int:
    """
    Delete User records that are:
      - email_verified=False AND phone_verified=False (never verified)
      - created_at older than retention period
      - have NO active (non-revoked, non-expired) sessions
      - is_active=True

    This utilizes a subquery EXISTS check to run in a single scalable transaction.
    """
    cutoff = _utcnow() - timedelta(days=settings.cleanup_unverified_user_days)
    now = _utcnow()

    active_session_exists = db.query(AuthSession).filter(
        AuthSession.user_id == User.id,
        AuthSession.revoked.is_(False),
        AuthSession.expires_at > now
    ).exists()

    deleted = (
        db.query(User)
        .filter(
            User.email_verified.is_(False),
            User.phone_verified.is_(False),
            User.is_active.is_(True),
            User.created_at < cutoff,
            ~active_session_exists
        )
        .delete(synchronize_session=False)
    )
    db.commit()
    logger.info("CLEANUP unverified_users deleted=%d", deleted)
    return deleted


def run_all_cleanup(db: DbSession) -> dict[str, int]:
    """
    Run all five cleanup functions and return a summary of deleted counts.
    Called by POST /internal/cleanup.
    """
    results = {
        "expired_verification_tokens": cleanup_expired_verification_tokens(db),
        "expired_password_reset_tokens": cleanup_expired_password_reset_tokens(db),
        "revoked_sessions": cleanup_revoked_sessions(db),
        "old_login_history": cleanup_old_login_history(db),
        "unverified_users": cleanup_unverified_users(db),
    }
    total = sum(results.values())
    logger.info("CLEANUP run_complete total_deleted=%d breakdown=%s", total, results)
    return results
