from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.core.security import verify_api_key

# Dependency shortcut for authenticated routes needing DB
async def get_authenticated_db(
    db: AsyncSession = Depends(get_db),
    _: str = Depends(verify_api_key)
):
    return db