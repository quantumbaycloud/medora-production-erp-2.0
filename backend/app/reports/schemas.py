from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from decimal import Decimal
from datetime import date

class DashboardKPIResponse(BaseModel):
    today_sales: Decimal
    today_purchase: Decimal
    monthly_sales: Decimal
    monthly_profit: Decimal
    total_customers: int
    total_medicines: int
    low_stock_count: int
    near_expiry_count: int
    outstanding_payments: Decimal
    pending_purchases: Decimal

class SalesReportItem(BaseModel):
    invoice_number: str
    date: str
    customer_name: Optional[str] = None
    payment_method: str
    total_amount: Decimal
    tax_amount: Decimal
    discount_amount: Decimal
    status: str

class ExpiryReportItem(BaseModel):
    medicine_name: str
    generic_name: Optional[str] = None
    batch_number: str
    expiry_date: str
    stock_available: int
    selling_price: Decimal
    status: str  # Expired, Near Expiry (<=30 days), Valid

class GSTReportItem(BaseModel):
    hsn_code: Optional[str] = None
    medicine_name: str
    taxable_value: Decimal
    gst_percentage: Decimal
    cgst_amount: Decimal
    sgst_amount: Decimal
    total_gst: Decimal
