from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, ConfigDict, Field

class CatalogOptionCreate(BaseModel):
    option_type: str = Field(min_length=2, max_length=60)
    code: str = Field(min_length=1, max_length=80)
    name: str = Field(min_length=1, max_length=160)
    is_active: bool = True
    sort_order: int = 0
    metadata: Optional[dict[str, Any]] = None

class CatalogOptionUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=160)
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None
    metadata: Optional[dict[str, Any]] = None

class CatalogOptionResponse(BaseModel):
    id: str
    pharmacy_id: str
    option_type: str
    code: str
    name: str
    is_active: bool
    sort_order: int
    metadata: Optional[dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)
