from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base, new_uuid


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=new_uuid)

    name = Column(String, nullable=True)
    username = Column(String(120), unique=True, nullable=True, index=True)
    email = Column(String, unique=True, nullable=True, index=True)
    phone = Column(String, unique=True, nullable=True, index=True)

    email_verified = Column(Boolean, default=False, nullable=False)
    phone_verified = Column(Boolean, default=False, nullable=False)

    # Account-level active flag. Distinct from employment / staff status.
    is_active = Column(Boolean, default=True, nullable=False)

    # Timestamp of the last password change.  The JWT middleware compares
    # the access token's `iat` claim against this value: any token issued
    # before a password change is immediately rejected even if it has not
    # yet expired.  Required by OWASP ASVS V2.2.7 / ADR-001-C.
    password_updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=True
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Auth relationships
    credential = relationship(
        "Credential", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    devices = relationship(
        "Device", back_populates="user", cascade="all, delete-orphan"
    )
    sessions = relationship(
        "Session", back_populates="user", cascade="all, delete-orphan"
    )
    login_histories = relationship(
        "LoginHistory", back_populates="user", cascade="all, delete-orphan"
    )
    email_verification_tokens = relationship(
        "EmailVerificationToken", back_populates="user", cascade="all, delete-orphan"
    )
    password_reset_tokens = relationship(
        "PasswordResetToken", back_populates="user", cascade="all, delete-orphan"
    )
    pharmacies = relationship(
        "Pharmacy", back_populates="owner", foreign_keys="[Pharmacy.owner_user_id]"
    )
