from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.schemas.payment import OrderCreate  # Import your clean schema here
from app.services import order_service

router = APIRouter()

@router.post("/create")
async def create_order(payload: OrderCreate, db: AsyncSession = Depends(get_db)):
    return await order_service.create_payment_order(
        db=db,
        gateway=payload.gateway,
        amount=payload.amount,
        receipt_id=payload.receipt_id
    )