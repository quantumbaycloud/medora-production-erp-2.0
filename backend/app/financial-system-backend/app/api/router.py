from fastapi import APIRouter
from app.api.endpoints import cashbook, bankbook, orders, webhooks

api_router = APIRouter()

api_router.include_router(cashbook.router, prefix="/cashbook", tags=["Cashbook"])
api_router.include_router(bankbook.router, prefix="/bankbook", tags=["Bankbook"])
api_router.include_router(orders.router, prefix="/orders", tags=["Orders & Payments"])
api_router.include_router(webhooks.router, prefix="/webhooks", tags=["Webhooks"])