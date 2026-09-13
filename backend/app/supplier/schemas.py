from pydantic import BaseModel, ConfigDict, EmailStr, Field, AliasChoices
from typing import Optional, Any
from decimal import Decimal

class SupplierBase(BaseModel):
    name: str = Field(..., validation_alias=AliasChoices('name', 'supplier_name'))
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    gstin: Optional[str] = Field(None, validation_alias=AliasChoices('gstin', 'gst'))
    drug_license: Optional[str] = None
    bank_name: Optional[str] = None
    account_number: Optional[str] = None
    ifsc_code: Optional[str] = None
    payment_terms: Optional[str] = None
    category_id: Optional[str] = None
    status: str = "active"
    description: Optional[str] = None
    pharmacy_id: Optional[str] = None

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(BaseModel):
    name: Optional[str] = Field(None, validation_alias=AliasChoices('name', 'supplier_name'))
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    gstin: Optional[str] = Field(None, validation_alias=AliasChoices('gstin', 'gst'))
    drug_license: Optional[str] = None
    bank_name: Optional[str] = None
    account_number: Optional[str] = None
    ifsc_code: Optional[str] = None
    payment_terms: Optional[str] = None
    category_id: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None
    pharmacy_id: Optional[str] = None

class SupplierResponse(SupplierBase):
    id: str
    pharmacy_id: Optional[str] = None
    created_at: Optional[Any] = None
    updated_at: Optional[Any] = None
    outstanding_balance: Optional[Decimal] = Decimal("0.00")
    category_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)