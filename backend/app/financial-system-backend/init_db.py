import asyncio
from app.database.session import engine
from app.database.base_class import Base

# Import all models so SQLAlchemy registers them before creating tables
from app.models.transactions import Order
from app.models.transactions import CashTransaction
from app.models.transactions import BankTransaction

async def create_tables():
    async with engine.begin() as conn:
        # This tells SQLAlchemy to create all tables that inherit from Base
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully!")

if __name__ == "__main__":
    asyncio.run(create_tables())