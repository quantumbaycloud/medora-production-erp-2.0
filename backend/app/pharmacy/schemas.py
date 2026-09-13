"""
app/pharmacy/schemas.py

Pydantic v2 request/response schemas for Pharmacy Profile management.

Enforces:
  - Whitespace stripping and empty string -> None normalization across all fields.
  - Statutory regex validation and uppercase normalization for Indian GST, PAN, and IFSC codes.
  - Normalization (`+91 9876543210` -> `+919876543210`) and validation (`10-15 digits`) for Indian/International phone numbers.
  - Strict EmailStr validation for email fields.
  - DRY validation mixin to eliminate duplicate validator logic across Create and Update schemas.
  - Realistic OpenAPI examples using Pydantic `json_schema_extra`.
"""

import re
from typing import Any
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


def normalize_optional_str(v: Any) -> str | None:
    """Strip whitespace and convert empty strings or whitespace-only strings to None."""
    if v is None or v == "" or (isinstance(v, str) and not v.strip()):
        return None
    if isinstance(v, str):
        return v.strip()
    return v


def validate_and_normalize_gst(v: Any) -> str | None:
    """Validate and normalize Indian GST number (e.g., 27AABCU9603R1ZM)."""
    if v is None or v == "" or (isinstance(v, str) and not v.strip()):
        return None
    if isinstance(v, str):
        v = v.strip().upper()
        if not re.match(r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$", v):
            raise ValueError("Invalid Indian GST number format (e.g., 27AABCU9603R1ZM)")
        return v
    raise ValueError("GST number must be a string")


def validate_and_normalize_pan(v: Any) -> str | None:
    """Validate and normalize Indian PAN number (e.g., AABCU9603R)."""
    if v is None or v == "" or (isinstance(v, str) and not v.strip()):
        return None
    if isinstance(v, str):
        v = v.strip().upper()
        if not re.match(r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$", v):
            raise ValueError("Invalid Indian PAN number format (e.g., AABCU9603R)")
        return v
    raise ValueError("PAN number must be a string")


def validate_and_normalize_ifsc(v: Any) -> str | None:
    """Validate and normalize Indian Bank IFSC code (e.g., SBIN0001234)."""
    if v is None or v == "" or (isinstance(v, str) and not v.strip()):
        return None
    if isinstance(v, str):
        v = v.strip().upper()
        if not re.match(r"^[A-Z]{4}0[A-Z0-9]{6}$", v):
            raise ValueError("Invalid Indian IFSC code format (e.g., SBIN0001234)")
        return v
    raise ValueError("IFSC code must be a string")


def validate_and_normalize_phone(v: Any) -> str | None:
    """
    Validate and normalize Indian/International phone numbers.
    Accepts formats such as:
      - +919876543210
      - +91 9876543210
      - +91-9876543210
      - 9876543210
    Normalizes by stripping spaces, hyphens, and parentheses while preserving optional '+' prefix.
    """
    if v is None or v == "" or (isinstance(v, str) and not v.strip()):
        return None
    if not isinstance(v, str):
        raise ValueError("Phone number must be a string")

    v_clean = v.strip()
    # Check for invalid characters before stripping allowed formatting separators
    if not re.match(r"^\+?[0-9\s\-()]+$", v_clean):
        raise ValueError("Invalid phone number format. Contains invalid characters.")

    has_plus = v_clean.startswith("+")
    digits = re.sub(r"[^0-9]", "", v_clean)

    if not (10 <= len(digits) <= 15):
        raise ValueError("Invalid phone number format. Must contain 10 to 15 digits.")

    return f"+{digits}" if has_plus else digits


class _PharmacyValidationMixin:
    """Shared validator mixin for Pharmacy create and update models to prevent duplicate logic."""

    @field_validator("gst_number", mode="before")
    @classmethod
    def _val_gst(cls, v: Any) -> Any:
        return validate_and_normalize_gst(v)

    @field_validator("pan_number", mode="before")
    @classmethod
    def _val_pan(cls, v: Any) -> Any:
        return validate_and_normalize_pan(v)

    @field_validator("bank_ifsc", mode="before")
    @classmethod
    def _val_ifsc(cls, v: Any) -> Any:
        return validate_and_normalize_ifsc(v)

    @field_validator("contact_phone", mode="before")
    @classmethod
    def _val_phone(cls, v: Any) -> Any:
        return validate_and_normalize_phone(v)

    @field_validator("contact_email", mode="before")
    @classmethod
    def _val_email(cls, v: Any) -> Any:
        return normalize_optional_str(v)

    @field_validator(
        "logo_path",
        "address",
        "bank_account_number",
        "bank_name",
        "drug_license_document_id",
        "gst_certificate_document_id",
        "pan_document_id",
        mode="before",
    )
    @classmethod
    def _val_opt_strs(cls, v: Any) -> Any:
        return normalize_optional_str(v)


class PharmacyCreate(_PharmacyValidationMixin, BaseModel):
    name: str = Field(..., min_length=1, max_length=150, description="Official legal or trade name of the pharmacy")
    logo_path: str | None = Field(None, max_length=500, description="CDN URL or storage path to the pharmacy logo image")
    gst_number: str | None = Field(None, max_length=15, description="15-character Indian Goods and Services Tax number")
    pan_number: str | None = Field(None, max_length=10, description="10-character Indian Permanent Account Number")
    address: str | None = Field(None, max_length=500, description="Physical postal address of the registered pharmacy")
    contact_phone: str | None = Field(None, max_length=20, description="Primary contact phone number (10-15 digits, E.164 or Indian format)")
    contact_email: EmailStr | None = Field(None, description="Primary contact email address for official communications")
    bank_account_number: str | None = Field(None, min_length=5, max_length=30, description="Bank account number for settlements")
    bank_ifsc: str | None = Field(None, max_length=11, description="11-character Indian Financial System Code (IFSC)")
    bank_name: str | None = Field(None, max_length=150, description="Name of the banking institution")
    drug_license_document_id: str | None = Field(None, max_length=150, description="Document identifier for uploaded Drug License certificate")
    gst_certificate_document_id: str | None = Field(None, max_length=150, description="Document identifier for uploaded GST registration certificate")
    pan_document_id: str | None = Field(None, max_length=150, description="Document identifier for uploaded PAN card copy")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Apex Care Pharmacy",
                "logo_path": "https://cdn.medorax.com/logos/apex-care.png",
                "gst_number": "27AABCU9603R1ZM",
                "pan_number": "AABCU9603R",
                "address": "Shop 12, Ground Floor, MG Road, Pune, Maharashtra 411001",
                "contact_phone": "+919876543210",
                "contact_email": "contact@apexcarepharma.in",
                "bank_account_number": "50200012345678",
                "bank_ifsc": "SBIN0001234",
                "bank_name": "State Bank of India",
                "drug_license_document_id": "doc_dl_987654",
                "gst_certificate_document_id": "doc_gst_987654",
                "pan_document_id": "doc_pan_987654",
            }
        }
    )

    @field_validator("name", mode="before")
    @classmethod
    def normalize_and_validate_name(cls, v: Any) -> Any:
        if v is None:
            raise ValueError("Name is required")
        if isinstance(v, str):
            v = v.strip()
            if not v:
                raise ValueError("Name cannot be empty or only whitespace")
            return v
        raise ValueError("Name must be a string")


class PharmacyUpdate(_PharmacyValidationMixin, BaseModel):
    name: str | None = Field(None, min_length=1, max_length=150, description="Official legal or trade name of the pharmacy")
    logo_path: str | None = Field(None, max_length=500, description="CDN URL or storage path to the pharmacy logo image")
    gst_number: str | None = Field(None, max_length=15, description="15-character Indian Goods and Services Tax number")
    pan_number: str | None = Field(None, max_length=10, description="10-character Indian Permanent Account Number")
    address: str | None = Field(None, max_length=500, description="Physical postal address of the registered pharmacy")
    contact_phone: str | None = Field(None, max_length=20, description="Primary contact phone number (10-15 digits)")
    contact_email: EmailStr | None = Field(None, description="Primary contact email address")
    bank_account_number: str | None = Field(None, min_length=5, max_length=30, description="Bank account number for settlements")
    bank_ifsc: str | None = Field(None, max_length=11, description="11-character Indian Financial System Code (IFSC)")
    bank_name: str | None = Field(None, max_length=150, description="Name of the banking institution")
    drug_license_document_id: str | None = Field(None, max_length=150, description="Document identifier for uploaded Drug License certificate")
    gst_certificate_document_id: str | None = Field(None, max_length=150, description="Document identifier for uploaded GST registration certificate")
    pan_document_id: str | None = Field(None, max_length=150, description="Document identifier for uploaded PAN card copy")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Apex Care Pharmacy & Surgical",
                "contact_phone": "+919876543211",
                "contact_email": "support@apexcarepharma.in",
                "address": "Shop 12-14, Ground Floor, MG Road, Pune, Maharashtra 411001",
            }
        }
    )

    @field_validator("name", mode="before")
    @classmethod
    def normalize_and_validate_name(cls, v: Any) -> Any:
        if v is None or v == "" or (isinstance(v, str) and not v.strip()):
            return None
        if isinstance(v, str):
            v = v.strip()
            if not v:
                raise ValueError("Name cannot be empty or only whitespace")
            return v
        raise ValueError("Name must be a string")


class PharmacyRead(BaseModel):
    id: str = Field(..., description="Unique UUID of the pharmacy record")
    owner_user_id: str = Field(..., description="UUID of the primary owner user")
    name: str = Field(..., description="Official legal or trade name of the pharmacy")
    logo_path: str | None = Field(None, description="CDN URL or storage path to the pharmacy logo image")
    gst_number: str | None = Field(None, description="15-character Indian Goods and Services Tax number")
    pan_number: str | None = Field(None, description="10-character Indian Permanent Account Number")
    address: str | None = Field(None, description="Physical postal address of the registered pharmacy")
    contact_phone: str | None = Field(None, description="Primary contact phone number")
    contact_email: str | None = Field(None, description="Primary contact email address")
    drug_license_document_id: str | None = Field(None, description="Document identifier for uploaded Drug License certificate")
    gst_certificate_document_id: str | None = Field(None, description="Document identifier for uploaded GST registration certificate")
    pan_document_id: str | None = Field(None, description="Document identifier for uploaded PAN card copy")
    # Bank details intentionally excluded from the default read response --
    # sensitive, and most callers (e.g. a branch list screen) don't need it.

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "11cb179b-5023-4182-b6c8-ebb26e74a0f7",
                "owner_user_id": "22cb179b-5023-4182-b6c8-ebb26e74a0f8",
                "name": "Apex Care Pharmacy",
                "logo_path": "https://cdn.medorax.com/logos/apex-care.png",
                "gst_number": "27AABCU9603R1ZM",
                "pan_number": "AABCU9603R",
                "address": "Shop 12, Ground Floor, MG Road, Pune, Maharashtra 411001",
                "contact_phone": "+919876543210",
                "contact_email": "contact@apexcarepharma.in",
                "drug_license_document_id": "doc_dl_987654",
                "gst_certificate_document_id": "doc_gst_987654",
                "pan_document_id": "doc_pan_987654",
            }
        },
    )
