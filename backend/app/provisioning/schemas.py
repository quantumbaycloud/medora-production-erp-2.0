from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class ProvisionUser(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None


class ProvisionBusiness(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    gst_number: str | None = None
    pan_number: str | None = None
    address: str | None = None
    contact_phone: str | None = None
    contact_email: str | None = None
    bank_account_number: str | None = None
    bank_ifsc: str | None = None
    bank_name: str | None = None


class ProvisionRequest(BaseModel):
    licenseKey: str = Field(min_length=1, max_length=128)
    licenseExpiresAt: Any
    license: dict[str, Any]
    licenseSignature: str = Field(min_length=16)
    pharmacyId: str = Field(min_length=1, max_length=128)
    erpUsername: str = Field(min_length=1, max_length=120)
    temporaryPassword: str = Field(min_length=8, max_length=255)
    user: ProvisionUser
    business: ProvisionBusiness


class ProvisionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    status: str
    externalId: str
    userId: str
    pharmacyId: str
    licenseId: str
