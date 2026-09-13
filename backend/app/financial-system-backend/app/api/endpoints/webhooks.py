from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
import json
from decimal import Decimal

from app.database.session import get_db
from app.database.base_class import TransactionType
from app.schemas.cashbook import CashTransactionCreate
from app.services import cashbook_service, bankbook_service
from app.services.payment_providers.razorpay import RazorpayProvider

router = APIRouter()
razorpay_provider = RazorpayProvider()

# ==========================================
# EXTERNAL PAYMENT GATEWAY WEBHOOKS
# ==========================================

@router.post("/razorpay")
async def razorpay_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    # 1. Get the signature from the headers
    signature = request.headers.get("x-razorpay-signature")
    if not signature:
        raise HTTPException(status_code=400, detail="Missing signature")

    # 2. Get the raw body of the request
    body = await request.body()
    payload = body.decode("utf-8")

    # 3. Verify the cryptographic signature
    is_valid = razorpay_provider.verify_webhook(payload, signature)
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # 4. If valid, process the payment
    data = json.loads(payload)
    event = data.get("event")
    
    if event == "payment.captured":
        payment_entity = data["payload"]["payment"]["entity"]
        order_id = payment_entity.get("order_id")
        transaction_id = payment_entity.get("id")
        amount_in_rupees = payment_entity.get("amount") / 100 
        
        # Save to our database
        await bankbook_service.record_gateway_settlement(
            db=db,
            order_id=order_id,
            gateway_txn_id=transaction_id,
            amount=amount_in_rupees
        )

    return {"status": "success"}

@router.post("/paytm")
async def paytm_webhook(request: Request):
    return {"status": "success"}

@router.post("/ccavenue")
async def ccavenue_webhook(request: Request):
    return {"status": "success"}


# ==========================================
# INTERNAL SYSTEM WEBHOOKS (DJANGO & SUPPLIER INTEGRATION)
# ==========================================

class InventorySyncEvent(BaseModel):
    medicine_name: str
    transaction_type: str
    quantity: int
    total_amount: float

class SupplierSyncEvent(BaseModel):
    supplier_name: str
    transaction_type: str = "purchase"
    total_amount: float
    remarks: str | None = None

@router.post("/internal/inventory-sync")
async def internal_inventory_webhook(event: InventorySyncEvent, db: AsyncSession = Depends(get_db)):
    print(f"\n🔔 [FINANCE SYSTEM] Received Inventory Sync!")
    print(f"Action: {event.transaction_type.upper()} | Item: {event.medicine_name}")
    print(f"Total Value to Record: ₹{event.total_amount}\n")
    
    tx_type = TransactionType.CREDIT if event.transaction_type.lower() == "sale" else TransactionType.DEBIT
    source = f"Inventory: {event.transaction_type.title()} ({event.medicine_name})"
    remarks = f"Automated sync for {event.quantity} units of {event.medicine_name}"
    
    if event.total_amount > 0:
        await cashbook_service.add_cash_entry(
            db=db,
            data=CashTransactionCreate(
                amount=Decimal(str(event.total_amount)),
                type=tx_type,
                source=source,
                remarks=remarks
            )
        )
    
    return {"status": "success", "message": "Data recorded in financial system"}

@router.post("/internal/supplier-sync")
async def internal_supplier_webhook(event: SupplierSyncEvent, db: AsyncSession = Depends(get_db)):
    print(f"\n🔔 [FINANCE SYSTEM] Received Supplier Sync!")
    print(f"Supplier: {event.supplier_name} | Amount: ₹{event.total_amount}\n")
    
    source = f"Supplier: {event.supplier_name}"
    remarks = event.remarks or f"Purchase order for {event.supplier_name}"
    
    if event.total_amount > 0:
        await cashbook_service.add_cash_entry(
            db=db,
            data=CashTransactionCreate(
                amount=Decimal(str(event.total_amount)),
                type=TransactionType.DEBIT,
                source=source,
                remarks=remarks
            )
        )
        
    return {"status": "success", "message": "Supplier transaction recorded in financial system"}