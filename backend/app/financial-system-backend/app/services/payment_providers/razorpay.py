import razorpay
from decimal import Decimal
from app.core.config import settings
from .base import PaymentProvider

class RazorpayProvider(PaymentProvider):
    def __init__(self):
        self.client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )
    async def create_order(self, amount: Decimal, receipt_id: str) -> dict:
        data = {
            "amount": int(amount * 100), # Razorpay expects paisa
            "currency": "INR",
            "receipt": receipt_id
        }
        return self.client.order.create(data=data)
    
    
    def verify_webhook(self, payload: dict, signature: str) -> bool:
        try:
            self.client.utility.verify_webhook_signature(
                payload, signature, settings.RAZORPAY_KEY_SECRET
            )
            return True
        except razorpay.errors.SignatureVerificationError:
            return False