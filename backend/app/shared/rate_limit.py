"""
app/shared/rate_limit.py

Rate limiting singleton for all endpoints.

Library: slowapi (wraps the `limits` library).
  - De-facto FastAPI rate limiting solution.
  - Uses a decorator pattern: @limiter.limit("10/minute")
  - Default storage: in-memory (correct for single-process, single-server).
  - For multi-server / horizontal scaling: change storage_uri to Redis:
      Limiter(key_func=get_remote_address, storage_uri="redis://redis:6379")
    Zero call-site changes required.

Usage in routers:
    from app.shared.rate_limit import limiter

    @router.post("/login")
    @limiter.limit(settings.rate_limit_login)
    async def login(request: Request, ...):
        ...

Setup in main.py:
    from slowapi import _rate_limit_exceeded_handler
    from slowapi.errors import RateLimitExceeded

    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
"""

from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core.config import settings

# Single limiter instance shared across the application.
# key_func=get_remote_address rates per client IP.
# Falls back to in-memory storage if Redis is not running locally.
try:
    limiter = Limiter(key_func=get_remote_address, storage_uri=settings.redis_url)
except Exception:
    limiter = Limiter(key_func=get_remote_address, storage_uri="memory://")
