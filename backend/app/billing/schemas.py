from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from decimal import Decimal
from datetime import datetime

# --- Item Schemas ---

class BillingItemRequest(BaseModel):
    medicine_id: str
    batch_number: Optional[str] = None
    quantity: int = Field(gt=0)
    discount_type: Optional[str] = Field(None, description="'percentage' or 'flat'")
    discount_value: Decimal = Field(default=Decimal("0.00"), ge=0)

class InvoiceItemResponse(BaseModel):
    id: str
    medicine_id: str
    medicine_name: str
    batch_number: str
    quantity: int
    rate: Decimal
    discount: Decimal
    gst_percentage: Decimal
    gst_amount: Decimal
    total_amount: Decimal

    model_config = ConfigDict(from_attributes=True)


# --- Invoice Schemas ---

class GenerateInvoiceRequest(BaseModel):
    customer_id: Optional[str] = None
    customer_name: Optional[str] = None
    branch_id: Optional[str] = None
    items: List[BillingItemRequest] = Field(min_length=1)
    payment_method: str = Field(default="Cash")  # Cash, Card, UPI, Wallet, Split Payment, Credit
    is_credit: bool = False
    cash_amount: Decimal = Field(default=Decimal("0.00"), ge=0)
    card_amount: Decimal = Field(default=Decimal("0.00"), ge=0)
    upi_amount: Decimal = Field(default=Decimal("0.00"), ge=0)
    wallet_amount: Decimal = Field(default=Decimal("0.00"), ge=0)

class QuickBillingRequest(BaseModel):
    medicine_id: str
    quantity: int = Field(gt=0)
    batch_number: Optional[str] = None
    payment_method: str = "Cash"
    branch_id: Optional[str] = None

class InvoiceResponse(BaseModel):
    id: str
    pharmacy_id: str
    branch_id: Optional[str] = None
    customer_id: Optional[str] = None
    invoice_number: str
    invoice_date: datetime
    customer_name: Optional[str] = None
    total_amount: Decimal
    discount_amount: Decimal
    tax_amount: Decimal
    payment_method: str
    payment_status: str
    items: List[InvoiceItemResponse] = []

    model_config = ConfigDict(from_attributes=True)


# --- Hold Bill Schemas ---

class HoldBillCreate(BaseModel):
    customer_id: Optional[str] = None
    customer_name: Optional[str] = None
    branch_id: Optional[str] = None
    items: List[BillingItemRequest] = Field(min_length=1)

class HoldBillResponse(BaseModel):
    id: str
    hold_number: str
    customer_name: Optional[str] = None
    total_amount: Decimal
    status: str
    created_at: datetime
    items: List[dict] = []


# --- Return & Exchange Schemas ---

class ReturnBillCreate(BaseModel):
    invoice_number: str
    medicine_id: str
    quantity: int = Field(gt=0)
    reason: Optional[str] = None
    branch_id: Optional[str] = None

class ReturnBillResponse(BaseModel):
    id: str
    invoice_number: str
    medicine_name: str
    quantity: int
    refund_amount: Decimal
    reason: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ExchangeBillCreate(BaseModel):
    invoice_number: str
    old_medicine_id: str
    old_quantity: int = Field(gt=0)
    new_medicine_id: str
    new_quantity: int = Field(gt=0)
    new_batch_number: Optional[str] = None
    branch_id: Optional[str] = None

class ExchangeBillResponse(BaseModel):
    id: str
    invoice_number: str
    old_medicine_name: str
    old_quantity: int
    new_medicine_name: str
    new_quantity: int
    price_difference: Decimal
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
