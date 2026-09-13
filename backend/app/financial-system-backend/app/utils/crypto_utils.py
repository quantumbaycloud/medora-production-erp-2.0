import hmac
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def generate_hmac_sha256(payload: str, secret: str) -> str:
    """Generates an HMAC-SHA256 hex string."""
    return hmac.new(
        secret.encode("utf-8"),
        payload.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

def aes_cbc_encrypt(plain_text: str, key_bytes: bytes, iv_bytes: bytes) -> str:
    """Encrypts text using AES-CBC (used by gateways like CCAvenue)."""
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
    padded_data = pad(plain_text.encode("utf-8"), AES.block_size)
    return cipher.encrypt(padded_data).hex()

def aes_cbc_decrypt(hex_cipher_text: str, key_bytes: bytes, iv_bytes: bytes) -> str:
    """Decrypts AES-CBC encrypted hex strings."""
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
    decrypted_padded = cipher.decrypt(bytes.fromhex(hex_cipher_text))
    return unpad(decrypted_padded, AES.block_size).decode("utf-8")