import paytmchecksum
from decimal import Decimal
from app.core.config import settings
from .base import PaymentProvider

class PaytmProvider(PaymentProvider):
    async def create_order(self, amount: Decimal, receipt_id: str) -> dict:
        paytm_params = {
            "MID": settings.PAYTM_MERCHANT_ID,
            "ORDER_ID": receipt_id,
            "TXN_AMOUNT": str(amount),
            "CUST_ID": f"CUST_{receipt_id}"
        }
        checksum = paytmchecksum.generateSignature(paytm_params, settings.PAYTM_MERCHANT_KEY)
        paytm_params["CHECKSUMHASH"] = checksum
        return paytm_params

    def verify_webhook(self, payload: dict, signature: str) -> bool:
        return paytmchecksum.verifySignature(payload, settings.PAYTM_MERCHANT_KEY, signature)