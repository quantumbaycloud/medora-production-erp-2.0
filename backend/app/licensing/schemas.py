from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field

class LicenseEnvelope(BaseModel):
    license: dict[str, Any]
    signature: str = Field(min_length=16)

class ActivationRequest(LicenseEnvelope):
    device_id: str = Field(min_length=8, max_length=255)
    device_name: str | None = Field(default=None, max_length=255)

class LicenseKeyActivationRequest(BaseModel):
    license_key: str = Field(min_length=4, max_length=128)

class DeactivationRequest(BaseModel):
    device_id: str = Field(min_length=8, max_length=255)

class LicenseStatus(BaseModel):
    license_id: str | None
    tenant_id: str | None
    plan: str | None
    status: str
    expires_at: datetime | None
    max_devices: int | None
    modules: list[str]
    device_id: str | None
    issuer_status: str | None = None
    offline_valid_until: datetime | None = None
