from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal

# --- PurchaseItem Schemas ---

class PurchaseItemBase(BaseModel):
    medicine_id: str
    batch_number: str
    expiry_date: date
    quantity: int = Field(gt=0)
    free_quantity: int = Field(default=0, ge=0)
    purchase_price: Decimal = Field(max_digits=10, decimal_places=2, ge=0)
    mrp: Decimal = Field(max_digits=10, decimal_places=2, ge=0)
    selling_price: Decimal = Field(max_digits=10, decimal_places=2, ge=0)
    tax_percentage: Decimal = Field(default=Decimal("0.00"), max_digits=10, decimal_places=2, ge=0)
    discount_percentage: Decimal = Field(default=Decimal("0.00"), max_digits=10, decimal_places=2, ge=0)

class PurchaseItemCreate(PurchaseItemBase):
    pass

class PurchaseItemResponse(PurchaseItemBase):
    id: str
    purchase_id: str
    total_amount: Decimal

    model_config = ConfigDict(from_attributes=True)


# --- PurchaseInvoice Schemas ---

class PurchaseInvoiceBase(BaseModel):
    supplier_id: str
    branch_id: Optional[str] = None
    invoice_number: str
    invoice_date: date
    notes: Optional[str] = None

class PurchaseInvoiceCreate(PurchaseInvoiceBase):
    paid_amount: Decimal = Field(default=Decimal("0.00"), max_digits=10, decimal_places=2, ge=0)
    items: List[PurchaseItemCreate] = Field(min_length=1)

class PurchaseInvoiceUpdate(BaseModel):
    supplier_id: Optional[str] = None
    branch_id: Optional[str] = None
    invoice_number: Optional[str] = None
    invoice_date: Optional[date] = None
    paid_amount: Optional[Decimal] = None
    notes: Optional[str] = None

class PurchaseInvoiceResponse(PurchaseInvoiceBase):
    id: str
    pharmacy_id: str
    total_amount: Decimal
    paid_amount: Decimal
    is_paid: bool
    status: str
    created_by_user_id: Optional[str] = None
    approved_by_user_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    items: List[PurchaseItemResponse] = []

    model_config = ConfigDict(from_attributes=True)
