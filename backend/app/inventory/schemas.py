from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime

class InventoryLedgerResponse(BaseModel):
    id: str
    pharmacy_id: str
    branch_id: Optional[str] = None
    medicine_id: str
    batch_number: str
    transaction_type: str
    quantity: int
    reference_id: Optional[str] = None
    notes: Optional[str] = None
    created_by_user_id: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class StockAdjustmentCreate(BaseModel):
    medicine_id: str
    batch_number: str
    quantity_delta: int = Field(description="Positive to add stock, negative to reduce/write-off")
    reason: str = Field(min_length=3, description="Reason for adjustment (e.g. damaged, audit discrepancy, expired)")

class ImportSummaryResponse(BaseModel):
    status: str
    total_processed: int
    successful: int
    failed: int
    errors: List[str] = []
