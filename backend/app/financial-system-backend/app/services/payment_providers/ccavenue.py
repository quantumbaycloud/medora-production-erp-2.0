from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
from decimal import Decimal
from app.core.config import settings
from .base import PaymentProvider

def get_ccavenue_cipher():
    # CCAvenue requires MD5 hash of the working key for the 16-byte AES key
    key = hashlib.md5(settings.CCAVENUE_WORKING_KEY.encode()).digest()
    # Specific IV designated by CCAvenue integration docs
    iv = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
    return AES.new(key, AES.MODE_CBC, iv)

class CCAvenueProvider(PaymentProvider):
    async def create_order(self, amount: Decimal, receipt_id: str) -> dict:
        # Prepare standard CCAvenue form parameters
        data = f"merchant_id={settings.CCAVENUE_MERCHANT_ID}&order_id={receipt_id}&amount={amount}&curreny=INR"
        
        cipher = get_ccavenue_cipher()
        encrypted_data = cipher.encrypt(pad(data.encode('utf-8'), 16)).hex()
        
        return {
            "access_code": settings.CCAVENUE_ACCESS_CODE,
            "encRequest": encrypted_data
        }

    def verify_webhook(self, payload: dict, signature: str = None) -> bool:
        # CCAvenue webhooks push an encrypted response payload instead of a signature header
        enc_response = payload.get("encResp")
        if not enc_response:
            return False
            
        try:
            cipher = get_ccavenue_cipher()
            decrypted = unpad(cipher.decrypt(bytes.fromhex(enc_response)), 16)
            # If it decrypts cleanly, it's authentically from CCAvenue
            return True
        except Exception:
            return False