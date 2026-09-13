from sqlalchemy.orm import Session
from app.customer.repository import CustomerRepository
from app.customer.schemas import CustomerCreateSchema

class CustomerService:
    def __init__(self, db: Session):
        self.repository = CustomerRepository(db)

    def get_customer_workspace_data(self, pharmacy_id: str, customer_type: str = "All Customers", search: str = None):
        return {
            "stats": self.repository.get_stats(pharmacy_id),
            "rows": self.repository.get_rows(pharmacy_id, customer_type, search),
        }

    def create_customer(self, pharmacy_id: str, data: CustomerCreateSchema):
        return self.repository.create_customer(pharmacy_id, data)

    def record_purchase(self, pharmacy_id: str, customer_name: str, spend_amount: float):
        return self.repository.record_purchase(pharmacy_id, customer_name, spend_amount)
