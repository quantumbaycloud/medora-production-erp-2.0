from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# asyncpg requires the postgresql+asyncpg:// driver in DATABASE_URL
engine = create_async_engine(settings.DATABASE_URL, echo=False)

SessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db():
    async with SessionLocal() as session:
        yield session