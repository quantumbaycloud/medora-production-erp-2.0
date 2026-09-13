from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated, Optional
from decimal import Decimal
from datetime import datetime
from app.database.base_class import TransactionType

class CashTransactionCreate(BaseModel):
    amount: Annotated[Decimal, Field(gt=0, decimal_places=2)]
    type: TransactionType
    source: str
    remarks: Optional[str] = None

class CashTransactionResponse(BaseModel):
    id: int
    amount: Annotated[Decimal, Field(decimal_places=2)]
    type: TransactionType
    source: str
    remarks: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)