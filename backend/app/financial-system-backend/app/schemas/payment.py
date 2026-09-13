from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated
from decimal import Decimal
from datetime import datetime

class OrderCreate(BaseModel):
    # Use Annotated and Field instead of condecimal
    amount: Annotated[Decimal, Field(gt=0, decimal_places=2)]
    gateway: str # "razorpay", "paytm", "ccavenue", etc.
    receipt_id: str

class OrderResponse(BaseModel):
    id: str
    gateway: str
    amount: Annotated[Decimal, Field(decimal_places=2)]
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)