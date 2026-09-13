from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from decimal import Decimal
from app.models.transactions import BankTransaction, Order
from app.database.base_class import TransactionType
from app.schemas.bankbook import BankTransactionCreate
from app.core.exceptions import DuplicateTransactionError, InsufficientBalanceError
from app.utils.logger import logger

async def add_manual_bank_entry(db: AsyncSession, data: BankTransactionCreate):
    """Processes manual bank entries (e.g. Bank charges, Wire transfers)."""
    if data.type.lower() == "debit":
        current = await get_bankbook_balance(db)
        if current["balance"] < data.amount:
            raise InsufficientBalanceError()

    transaction = BankTransaction(
        gateway_transaction_id=f"MANUAL_{data.source}_{int(data.amount * 100)}",
        amount=data.amount,
        type=data.type,
        created_at=func.now()
    )
    db.add(transaction)
    await db.commit()
    await db.refresh(transaction)
    logger.info(f"Manual bank entry recorded: {transaction.id}")
    return transaction

async def record_gateway_settlement(
    db: AsyncSession, 
    order_id: str, 
    gateway_txn_id: str, 
    amount: Decimal
):
    """Automatically records inbound customer payment settlements."""
    existing_txn = await db.scalar(
        select(BankTransaction).where(BankTransaction.gateway_transaction_id == gateway_txn_id)
    )
    if existing_txn:
        raise DuplicateTransactionError(gateway_txn_id)

    order = await db.scalar(select(Order).where(Order.id == order_id))
    if order:
        order.status = "paid"

    bank_entry = BankTransaction(
        order_id=order_id,
        gateway_transaction_id=gateway_txn_id,
        amount=amount,
        type=TransactionType.CREDIT
    )
    db.add(bank_entry)
    await db.commit()
    await db.refresh(bank_entry)
    logger.info(f"Bankbook credited via gateway: {gateway_txn_id} Amount: {amount}")
    return bank_entry

async def get_bankbook_balance(db: AsyncSession):
    """Computes total bank inflows, outflows, and net ledger balance."""
    result = await db.execute(
        select(BankTransaction.type, func.sum(BankTransaction.amount))
        .group_by(BankTransaction.type)
    )
    totals = dict(result.all())
    credit = totals.get(TransactionType.CREDIT, Decimal("0.00")) or Decimal("0.00")
    debit = totals.get(TransactionType.DEBIT, Decimal("0.00")) or Decimal("0.00")
    return {
        "balance": credit - debit,
        "total_credit": credit,
        "total_debit": debit
    }