from abc import ABC, abstractmethod
from decimal import Decimal

class PaymentProvider(ABC):
    @abstractmethod
    async def create_order(self, amount: Decimal, receipt_id: str)->dict:
        """Creates an order payload for the frontend."""
        pass

    @abstractmethod
    def verify_webhook(self, payload:dict, signature:str)->bool:
        """Verifies the authenticity of a webhook request."""
        pass