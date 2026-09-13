from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.customer.models import Customer
from app.customer.schemas import CustomerCreateSchema

class CustomerRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_stats(self, pharmacy_id: str):
        q = self.db.query(Customer).filter(Customer.pharmacy_id == pharmacy_id)
        total_customers = q.count()
        total_revenue = q.with_entities(func.sum(Customer.spend)).scalar() or 0.0
        repeat_customers = q.filter(Customer.orders > 1).count()
        repeat_rate = (repeat_customers / total_customers * 100) if total_customers else 0.0
        return {
            "customers": f"{total_customers:,}",
            "revenue": f"₹{total_revenue:,.0f}",
            "repeatRate": f"{repeat_rate:.0f}%",
        }

    def get_rows(self, pharmacy_id: str, customer_type: str = "All Customers", search: str = None):
        query = self.db.query(Customer).filter(Customer.pharmacy_id == pharmacy_id)
        if customer_type and customer_type != "All Customers":
            ctype_lower = customer_type.strip().lower()
            if ctype_lower == "repeat":
                query = query.filter(Customer.orders > 1)
            elif ctype_lower in {"one-time", "one time"}:
                query = query.filter(Customer.orders == 1)
            else:
                query = query.filter(Customer.type.ilike(customer_type.strip()))
        if search and search.strip():
            term = f"%{search.strip()}%"
            query = query.filter(
                (Customer.name.ilike(term)) |
                (Customer.customer_name.ilike(term)) |
                (Customer.type.ilike(term)) |
                (Customer.phone.ilike(term))
            )
        rows = query.order_by(Customer.updated_at.desc(), Customer.orders.desc()).all()
        return [
            {
                "id": str(c.id),
                "name": c.name or c.customer_name or "Unnamed Customer",
                "type": c.type or "Regular",
                "orders": c.orders or 0,
                "spend": f"₹{(c.spend or 0.0):,.0f}",
                "lastPurchase": c.last_purchase.strftime("%b %d, %Y") if c.last_purchase else "N/A",
            }
            for c in rows
        ]

    def create_customer(self, pharmacy_id: str, data: CustomerCreateSchema):
        cname = data.name.strip()
        customer = Customer(
            pharmacy_id=pharmacy_id,
            customer_name=cname,
            name=cname,
            type=data.type or "Regular",
            phone=data.phone,
            mobile_number=data.phone,
            email=data.email,
            orders=0,
            spend=0.0,
            last_purchase=None,
        )
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        return customer

    def record_purchase(self, pharmacy_id: str, customer_name: str, spend_amount: float):
        if not customer_name:
            return None
        cname = customer_name.strip()
        customer = self.db.query(Customer).filter(
            Customer.pharmacy_id == pharmacy_id,
            (Customer.name.ilike(cname)) | (Customer.customer_name.ilike(cname)),
        ).first()
        now = datetime.now(timezone.utc)
        if customer:
            customer.orders = (customer.orders or 0) + 1
            customer.spend = (customer.spend or 0.0) + float(spend_amount)
            customer.last_purchase = now
            customer.type = "VIP" if customer.orders >= 10 else ("Regular" if customer.orders > 1 else "New")
        else:
            customer = Customer(
                pharmacy_id=pharmacy_id,
                customer_name=cname,
                name=cname,
                type="New",
                orders=1,
                spend=float(spend_amount),
                last_purchase=now,
            )
            self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        return customer
