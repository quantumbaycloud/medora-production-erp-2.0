import hmac
import hashlib
from decimal import Decimal
from app.core.config import settings
from .base import PaymentProvider

class PineLabsProvider(PaymentProvider):
    async def create_order(self, amount: Decimal, receipt_id: str) -> dict:
        # Returns data required to initiate a Plutus/Edge request
        return {"amount": int(amount * 100), "order_id": receipt_id}

    def verify_webhook(self, payload_string: str, signature: str) -> bool:
        # Pine Labs uses HMAC SHA256 of the raw payload string
        expected_sig = hmac.new(
            settings.PINELABS_SECRET.encode(),
            payload_string.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return expected_sig.upper() == signature.upper()