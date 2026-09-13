from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated, Optional
from decimal import Decimal
from datetime import datetime
from app.database.base_class import TransactionType

class BankTransactionCreate(BaseModel):
    amount: Annotated[Decimal, Field(gt=0, decimal_places=2)]
    type: TransactionType
    source: str 
    remarks: Optional[str] = None

class BankTransactionResponse(BaseModel):
    id: int
    order_id: Optional[str]
    gateway_transaction_id: str
    amount: Annotated[Decimal, Field(decimal_places=2)]
    type: TransactionType
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)