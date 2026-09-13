from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.transactions import CashTransaction
from app.database.base_class import TransactionType
from app.schemas.cashbook import CashTransactionCreate

async def add_cash_entry(db: AsyncSession, data: CashTransactionCreate):
    transaction = CashTransaction(
        amount=data.amount,
        type=data.type.value if hasattr(data.type, 'value') else str(data.type),
        source=data.source,
        remarks=data.remarks
    )
    db.add(transaction)
    await db.commit()
    await db.refresh(transaction)
    return transaction

async def get_cashbook_balance(db: AsyncSession):
    result = await db.execute(
        select(CashTransaction.type, func.sum(CashTransaction.amount))
        .group_by(CashTransaction.type)
    )
    totals = dict(result.all())
    credit = totals.get(TransactionType.CREDIT, 0)
    debit = totals.get(TransactionType.DEBIT, 0)
    return {"balance": credit - debit, "total_in": credit, "total_out": debit}