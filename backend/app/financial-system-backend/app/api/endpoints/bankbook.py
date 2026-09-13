from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.schemas.bankbook import BankTransactionCreate
from app.services import bankbook_service

router = APIRouter()

@router.post("/entry")
async def create_bank_entry(data: BankTransactionCreate, db: AsyncSession = Depends(get_db)):
    return await bankbook_service.add_manual_bank_entry(db, data)

@router.get("/balance")
async def get_balance(db: AsyncSession = Depends(get_db)):
    return await bankbook_service.get_bankbook_balance(db)