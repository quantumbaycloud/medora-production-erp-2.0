from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.schemas.cashbook import CashTransactionCreate
from app.services import cashbook_service

router = APIRouter()

@router.post("/entry")
async def create_cash_entry(data: CashTransactionCreate, db: AsyncSession = Depends(get_db)):
    return await cashbook_service.add_cash_entry(db, data)

@router.get("/balance")
async def get_balance(db: AsyncSession = Depends(get_db)):
    return await cashbook_service.get_cashbook_balance(db)