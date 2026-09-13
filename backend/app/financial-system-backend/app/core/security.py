import hmac
import hashlib
import secrets
from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from app.core.config import settings

API_KEY_HEADER = APIKeyHeader(name="X-API-KEY", auto_error=False)

def verify_api_key(api_key: str = Security(API_KEY_HEADER)) -> str:
    """Protects internal admin routes with an API key."""
    if not api_key or not secrets.compare_digest(api_key, settings.API_SECRET_KEY):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials"
        )
    return api_key

def secure_compare(a: str, b: str) -> bool:
    """Prevents timing attacks when verifying checksums and signatures."""
    return hmac.compare_digest(a.encode("utf-8"), b.encode("utf-8"))