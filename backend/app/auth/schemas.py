"""
app/auth/schemas.py

Pydantic v2 request/response schemas for authentication, device management,
and session lifecycle endpoints.
"""

import re
from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
    model_validator,
)


# ---------------------------------------------------------------------------
# Validators & Normalizers
# ---------------------------------------------------------------------------

def validate_password_strength(password: str) -> str:
    """
    Enforce password policy (OWASP ASVS V2.1.1):
      - Minimum 8 characters
      - At least one uppercase letter
      - At least one lowercase letter
      - At least one digit
      - At least one special/symbol character
    """
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long.")
    if not re.search(r"[A-Z]", password):
        raise ValueError("Password must contain at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        raise ValueError("Password must contain at least one lowercase letter.")
    if not re.search(r"\d", password):
        raise ValueError("Password must contain at least one digit.")
    # Matches any non-alphanumeric, non-whitespace character (including _, -, +, =, etc.)
    if not re.search(r"[^\w\s]|_", password):
        raise ValueError("Password must contain at least one special character.")
    return password


def validate_and_normalize_phone(phone: str | None) -> str | None:
    """
    Validates Indian 10-digit mobile numbers and normalizes to standard +91XXXXXXXXXX format.
    """
    if phone is None:
        return None
    phone = re.sub(r"[\s\-()]", "", phone)  # Strip spaces, dashes, parentheses
    if not phone:
        return None

    match = re.fullmatch(r"^(?:\+91|91)?([6-9]\d{9})$", phone)
    if not match:
        raise ValueError("Invalid phone number. Must be a valid 10-digit Indian mobile number.")
    
    # Standardize to E.164 format (+91XXXXXXXXXX)
    return f"+91{match.group(1)}"


def normalize_identifier(identifier: str) -> str:
    """Strips whitespace and standardizes emails/phones for login & reset queries."""
    clean = identifier.strip()
    if "@" in clean:
        return clean.lower()
    # If it looks like a phone number, normalize it
    try:
        return validate_and_normalize_phone(clean) or clean
    except ValueError:
        return clean


# ---------------------------------------------------------------------------
# Registration & Verification
# ---------------------------------------------------------------------------

class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr | None = Field(default=None, description="User's email address")
    phone: str | None = Field(default=None, description="User's 10-digit Indian mobile number")
    password: str = Field(..., min_length=8, description="Plaintext password conforming to OWASP ASVS")

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "Noman Ahmad",
                    "email": "noman@example.com",
                    "phone": "+919876543210",
                    "password": "SecurePass1!",
                }
            ]
        }
    )

    @field_validator("name", mode="before")
    @classmethod
    def strip_name(cls, v: str) -> str:
        if isinstance(v, str):
            v = v.strip()
            if not v:
                raise ValueError("Name cannot be empty or blank.")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        return validate_password_strength(value)

    @field_validator("phone", mode="before")
    @classmethod
    def validate_phone(cls, value: str | None) -> str | None:
        return validate_and_normalize_phone(value)

    @model_validator(mode="after")
    def validate_identifiers(self) -> "RegisterRequest":
        if not self.email and not self.phone:
            raise ValueError("Either email or phone must be provided for registration.")
        return self


class VerifyEmailRequest(BaseModel):
    token: str = Field(..., min_length=1, description="URL-safe verification token")

    model_config = ConfigDict(
        json_schema_extra={"examples": [{"token": "V9xKz2RwA_urlsafe_token"}]}
    )


class ResendVerificationRequest(BaseModel):
    email: EmailStr

    model_config = ConfigDict(
        json_schema_extra={"examples": [{"email": "noman@example.com"}]}
    )


# ---------------------------------------------------------------------------
# Password Reset
# ---------------------------------------------------------------------------

class ForgotPasswordRequest(BaseModel):
    identifier: str = Field(..., min_length=1, description="Registered email address or phone number")

    model_config = ConfigDict(
        json_schema_extra={"examples": [{"identifier": "noman@example.com"}]}
    )

    @field_validator("identifier", mode="before")
    @classmethod
    def normalize_id(cls, v: str) -> str:
        if isinstance(v, str):
            return normalize_identifier(v)
        return v


class ResetPasswordRequest(BaseModel):
    token: str = Field(..., min_length=1, description="URL-safe password reset token")
    password: str = Field(..., min_length=8, description="New password conforming to policy")

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "token": "V9xKz2RwA_urlsafe_token",
                    "password": "NewSecurePass1!",
                }
            ]
        }
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        return validate_password_strength(v)


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------

PlatformType = Literal["web", "android", "ios", "windows", "macos", "linux"]


class LoginRequest(BaseModel):
    identifier: str = Field(..., description="Registered email address or phone number")
    password: str = Field(..., description="Account password")

    device_identifier: UUID | None = Field(
        default=None,
        description=(
            "Stable UUID identifying this client installation. "
            "Generated by the client and persisted in secure storage. "
            "Send on every login to enforce one-session-per-device."
        ),
    )
    device_name: str | None = Field(default=None, max_length=255, description="e.g. 'iPhone 15 Pro', 'DESKTOP-ABC123'")
    platform: PlatformType = Field(default="web", description="Client platform")
    app_version: str | None = Field(default=None, max_length=50, description="Native app build/version")
    push_token: str | None = Field(default=None, description="FCM or APNs push notification token")

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "identifier": "noman@example.com",
                    "password": "SecurePass1!",
                    "device_identifier": "550e8400-e29b-41d4-a716-446655440000",
                    "device_name": "iPhone 15 Pro",
                    "platform": "ios",
                    "app_version": "2.1.0",
                }
            ]
        }
    )

    @field_validator("identifier", mode="before")
    @classmethod
    def normalize_id(cls, v: str) -> str:
        if isinstance(v, str):
            return normalize_identifier(v)
        return v


class RefreshRequest(BaseModel):
    refresh_token: str = Field(..., description="Active refresh token")

    model_config = ConfigDict(
        json_schema_extra={"examples": [{"refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}]}
    )


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: dict | None = None
    device_identifier: str | None = Field(
        default=None,
        description="Stable device UUID to persist for session continuity.",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "token_type": "bearer",
                    "device_identifier": "550e8400-e29b-41d4-a716-446655440000",
                }
            ]
        }
    )


# ---------------------------------------------------------------------------
# Device Schemas
# ---------------------------------------------------------------------------

class DeviceRead(BaseModel):
    id: str
    device_identifier: str
    platform: str
    device_name: str
    friendly_name: str | None = None
    browser: str | None = None
    operating_system: str | None = None
    app_version: str | None = None
    trusted: bool
    is_active: bool
    first_seen_at: datetime
    last_seen_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DeviceInSession(BaseModel):
    """Minimal device summary nested inside session responses."""
    id: str
    device_name: str
    friendly_name: str | None = None
    platform: str
    browser: str | None = None
    operating_system: str | None = None

    model_config = ConfigDict(from_attributes=True)


class DeviceUpdate(BaseModel):
    friendly_name: str | None = Field(default=None, max_length=255)
    trusted: bool | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"friendly_name": "My Work Laptop", "trusted": True}]
        }
    )


# ---------------------------------------------------------------------------
# Session Schemas
# ---------------------------------------------------------------------------

class SessionRead(BaseModel):
    id: str
    ip_address: str | None = None
    user_agent: str | None = None
    created_at: datetime
    last_activity_at: datetime | None = None
    expires_at: datetime
    device: DeviceInSession | None = None
    is_current: bool = False

    model_config = ConfigDict(from_attributes=True)