import time
from decimal import Decimal
from app.core.config import settings
from app.utils.crypto_utils import generate_hmac_sha256
from app.core.security import secure_compare
from .base import PaymentProvider

class BillDeskProvider(PaymentProvider):
    async def create_order(self, amount: Decimal, receipt_id: str) -> dict:
        timestamp = str(int(time.time()))
        order_payload = {
            "mercid": settings.BILLDESK_MERCHANT_ID,
            "orderid": receipt_id,
            "amount": str(amount),
            "order_date": timestamp,
            "currency": "356", # Currency code for INR
            "itemcode": "DIRECT",
            "device": {"init_channel": "internet", "ip": "127.0.0.1"}
        }

        # Format message string: mercid|orderid|amount|...
        raw_token = f"{settings.BILLDESK_MERCHANT_ID}|{receipt_id}|{amount}|{timestamp}"
        signature = generate_hmac_sha256(raw_token, settings.BILLDESK_SECRET_KEY)
        
        return {
            "order_payload": order_payload,
            "bdorderid": f"BD_{receipt_id}",
            "signature": signature
        }

    def verify_webhook(self, payload: dict, signature: str) -> bool:
        # Construct verification string according to BillDesk callback parameters
        raw_str = f"{payload.get('mercid')}|{payload.get('orderid')}|{payload.get('amount')}|{payload.get('status')}"
        expected_sig = generate_hmac_sha256(raw_str, settings.BILLDESK_SECRET_KEY)
        return secure_compare(expected_sig, signature)