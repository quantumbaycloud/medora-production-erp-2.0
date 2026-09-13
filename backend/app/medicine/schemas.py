from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import date
from decimal import Decimal

# --- MedicineBatch Schemas ---

class MedicineBatchBase(BaseModel):
    batch_number: str
    expiry_date: date
    purchase_price: Decimal = Field(max_digits=10, decimal_places=2)
    selling_price: Decimal = Field(max_digits=10, decimal_places=2)
    mrp: Decimal = Field(max_digits=10, decimal_places=2)
    quantity_available: int
    status: str = "ACTIVE"

class MedicineBatchCreate(MedicineBatchBase):
    pass

class MedicineBatchUpdate(BaseModel):
    expiry_date: Optional[date] = None
    purchase_price: Optional[Decimal] = None
    selling_price: Optional[Decimal] = None
    mrp: Optional[Decimal] = None
    quantity_available: Optional[int] = None
    status: Optional[str] = None

class MedicineBatchResponse(MedicineBatchBase):
    id: str
    medicine_id: str
    model_config = ConfigDict(from_attributes=True)


# --- Medicine Schemas ---

class MedicineBase(BaseModel):
    name: str
    generic_name: Optional[str] = None
    brand_name: Optional[str] = None
    manufacturer: Optional[str] = None
    category: Optional[str] = None
    unit: Optional[str] = None
    barcode: Optional[str] = None
    sku: Optional[str] = None
    schedule_type: Optional[str] = None
    hsn_code: Optional[str] = None
    gst_percentage: Optional[Decimal] = None
    min_stock_level: int = 0
    rack: Optional[str] = None

class MedicineCreate(MedicineBase):
    pass

class MedicineUpdate(BaseModel):
    name: Optional[str] = None
    generic_name: Optional[str] = None
    brand_name: Optional[str] = None
    manufacturer: Optional[str] = None
    category: Optional[str] = None
    unit: Optional[str] = None
    barcode: Optional[str] = None
    sku: Optional[str] = None
    schedule_type: Optional[str] = None
    hsn_code: Optional[str] = None
    gst_percentage: Optional[Decimal] = None
    min_stock_level: Optional[int] = None
    rack: Optional[str] = None

class MedicineResponse(MedicineBase):
    id: str
    pharmacy_id: str
    batches: List[MedicineBatchResponse] = []
    
    model_config = ConfigDict(from_attributes=True)
