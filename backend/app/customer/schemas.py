from pydantic import BaseModel
from typing import List, Optional

class CustomerStatsSchema(BaseModel):
    customers: str
    revenue: str
    repeatRate: str

class CustomerRowSchema(BaseModel):
    id: Optional[str] = None
    name: str
    type: str
    orders: int
    spend: str
    lastPurchase: str

class CustomerResponseSchema(BaseModel):
    stats: CustomerStatsSchema
    rows: List[CustomerRowSchema]

class CustomerCreateSchema(BaseModel):
    name: str
    type: Optional[str] = "Regular"
    phone: Optional[str] = None
    email: Optional[str] = None
    orders: Optional[int] = 1
    spend: Optional[float] = 0.0