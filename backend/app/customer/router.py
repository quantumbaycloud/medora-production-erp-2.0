from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from app.customer.schemas import CustomerResponseSchema, CustomerCreateSchema
from app.customer.service import CustomerService
from app.db.base import get_db
from app.licensing.deps import get_current_licensed_user
from app.staff.service import get_current_pharmacy_id
from app.staff.permissions import Permissions
from app.user.models import User

router = APIRouter(prefix="/api/customers", tags=["Customers"])

@router.get("/", response_model=CustomerResponseSchema)
def get_customer_data(
    customerType: str = Query("All Customers"),
    search: Optional[str] = Query(None),
    pharmacy_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user),
):
    active = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.CUSTOMER_READ.code)
    return CustomerService(db).get_customer_workspace_data(active, customerType, search)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_customer(
    payload: CustomerCreateSchema,
    pharmacy_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_licensed_user),
):
    active = get_current_pharmacy_id(db, current_user.id, pharmacy_id, Permissions.CUSTOMER_MANAGE.code)
    return CustomerService(db).create_customer(active, payload)
