"""
app/branch/schemas.py

Pydantic v2 request/response schemas for Branch Management.

Enforces:
  - Whitespace stripping and empty string -> None normalization across optional fields.
  - Normalization (+91 9876543210 -> +919876543210) and validation (10-15 digits) for phone numbers.
  - Strict validation on required/optional names.
  - DRY validation mixin sharing core normalizers with Pharmacy schemas.
  - Realistic OpenAPI examples using Pydantic json_schema_extra.
"""

import json
from typing import Any
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.branch.models import BRANCH_STATUSES
from app.pharmacy.schemas import normalize_optional_str, validate_and_normalize_phone


class _BranchValidationMixin:
    """Shared validator mixin for Branch create and update models to prevent duplicate logic."""

    @field_validator("contact_phone", mode="before")
    @classmethod
    def _val_phone(cls, v: Any) -> Any:
        return validate_and_normalize_phone(v)

    @field_validator("address", mode="before")
    @classmethod
    def _val_opt_strs(cls, v: Any) -> Any:
        return normalize_optional_str(v)

    @field_validator("settings_json", mode="before")
    @classmethod
    def _val_settings_json(cls, v: Any) -> str | None:
        normalized = normalize_optional_str(v)
        if normalized is None:
            return None
        # Ensure it is valid JSON if provided
        try:
            json.loads(normalized)
        except (ValueError, TypeError):
            raise ValueError("settings_json must be a valid JSON string")
        return normalized


class BranchCreate(_BranchValidationMixin, BaseModel):
    name: str = Field(
        ..., 
        min_length=1, 
        max_length=150, 
        description="Internal or commercial name of the branch location"
    )
    address: str | None = Field(
        None, 
        max_length=500, 
        description="Physical street address of this branch"
    )
    contact_phone: str | None = Field(
        None, 
        max_length=20, 
        description="Branch-specific contact phone number (10-15 digits)"
    )
    settings_json: str | None = Field(
        None, 
        max_length=10000, 
        description="JSON serialized configuration string for branch-specific toggles"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "MG Road Main Branch",
                    "address": "Ground Floor, Shop 12, MG Road, Pune, Maharashtra 411001",
                    "contact_phone": "+919876543210",
                    "settings_json": '{"billing_mode": "retail", "allow_credit": false}',
                }
            ]
        }
    )

    @field_validator("name", mode="before")
    @classmethod
    def normalize_and_validate_name(cls, v: Any) -> str:
        if v is None:
            raise ValueError("Name is required")
        if isinstance(v, str):
            v = v.strip()
            if not v:
                raise ValueError("Name cannot be empty or only whitespace")
            return v
        raise ValueError("Name must be a string")


class BranchUpdate(_BranchValidationMixin, BaseModel):
    name: str | None = Field(
        None, 
        min_length=1, 
        max_length=150, 
        description="Internal or commercial name of the branch location"
    )
    address: str | None = Field(
        None, 
        max_length=500, 
        description="Physical street address of this branch"
    )
    contact_phone: str | None = Field(
        None, 
        max_length=20, 
        description="Branch-specific contact phone number (10-15 digits)"
    )
    settings_json: str | None = Field(
        None, 
        max_length=10000, 
        description="JSON serialized configuration string for branch-specific toggles"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "MG Road Flagship Branch",
                    "contact_phone": "+919876543212",
                    "settings_json": '{"billing_mode": "retail", "allow_credit": true}',
                }
            ]
        }
    )

    @field_validator("name", mode="before")
    @classmethod
    def normalize_and_validate_name(cls, v: Any) -> str | None:
        if v is None:
            return None
        if isinstance(v, str):
            v = v.strip()
            if not v:
                raise ValueError("Name cannot be empty or only whitespace")
            return v
        raise ValueError("Name must be a string")


class BranchStatusUpdate(BaseModel):
    status: str = Field(
        ..., 
        description="Operational status of the branch ('active' or 'inactive')"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"status": "inactive"}]
        }
    )

    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, v: Any) -> str:
        if isinstance(v, str):
            v = v.strip().lower()
        if v not in BRANCH_STATUSES:
            raise ValueError(f"status must be one of {BRANCH_STATUSES}")
        return v


class BranchRead(BaseModel):
    id: str = Field(..., description="Unique UUID of the branch record")
    pharmacy_id: str = Field(..., description="UUID of the parent pharmacy")
    name: str = Field(..., description="Internal or commercial name of the branch location")
    address: str | None = Field(None, description="Physical street address of this branch")
    contact_phone: str | None = Field(None, description="Branch-specific contact phone number")
    settings_json: str | None = Field(None, description="JSON serialized configuration string for branch-specific toggles")
    status: str = Field(..., description="Operational status ('active' or 'inactive')")
    is_active: bool = Field(..., description="Boolean flag indicating whether the branch is active and visible in operations")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "id": "33cb179b-5023-4182-b6c8-ebb26e74a0f9",
                    "pharmacy_id": "11cb179b-5023-4182-b6c8-ebb26e74a0f7",
                    "name": "MG Road Main Branch",
                    "address": "Ground Floor, Shop 12, MG Road, Pune, Maharashtra 411001",
                    "contact_phone": "+919876543210",
                    "settings_json": '{"billing_mode": "retail", "allow_credit": false}',
                    "status": "active",
                    "is_active": True,
                }
            ]
        },
    )