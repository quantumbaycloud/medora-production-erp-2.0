from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal
from app.models.transactions import Order
from app.services.payment_providers.razorpay import RazorpayProvider
from app.services.payment_providers.paytm import PaytmProvider
from app.services.payment_providers.ccavenue import CCAvenueProvider
from app.services.payment_providers.pinelabs import PineLabsProvider
from app.services.payment_providers.billdesk import BillDeskProvider

PROVIDERS = {
    "razorpay": RazorpayProvider(),
    "paytm": PaytmProvider(),
    "ccavenue": CCAvenueProvider(),
    "pinelabs": PineLabsProvider(),
    "billdesk": BillDeskProvider()
}

async def create_payment_order(db: AsyncSession, gateway: str, amount: Decimal, receipt_id: str):
    gateway_key = gateway.lower()
    provider = PROVIDERS.get(gateway_key)
    if not provider:
        raise ValueError(f"Unsupported payment gateway: {gateway}")

    # Generate gateway order payload
    gateway_data = await provider.create_order(amount, receipt_id)

    # Persist pending order to database
    order = Order(
        id=receipt_id,
        gateway=gateway_key,
        amount=amount,
        status="created"
    )
    db.add(order)
    await db.commit()
    await db.refresh(order)

    return {
        "order": order,
        "gateway_response": gateway_data
    }