from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class NotificationResponse(BaseModel):
    id: str
    pharmacy_id: str
    branch_id: Optional[str] = None
    title: str
    message: str
    alert_type: str
    severity: str
    is_read: bool
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class NotificationCreate(BaseModel):
    title: str
    message: str
    alert_type: str
    severity: str = "INFO"
    branch_id: Optional[str] = None
    user_id: Optional[str] = None
