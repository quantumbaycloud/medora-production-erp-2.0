from sqlalchemy import Column, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.db.base import Base, new_uuid


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(String, primary_key=True, default=new_uuid)
    pharmacy_id = Column(
        String,
        ForeignKey("pharmacies.id"),
        nullable=False,
        index=True,
    )

    name = Column(String, nullable=False, index=True)
    contact_person = Column(String, nullable=True)
    phone = Column(String, nullable=True, index=True)
    email = Column(String, nullable=True)
    gstin = Column(String, nullable=True, index=True)
    address = Column(String, nullable=True)

    drug_license = Column(String, nullable=True)
    bank_name = Column(String, nullable=True)
    account_number = Column(String, nullable=True)
    ifsc_code = Column(String, nullable=True)
    payment_terms = Column(String, nullable=True)
    category_id = Column(String, ForeignKey("catalog_options.id", ondelete="SET NULL"), nullable=True, index=True)
    status = Column(String(30), nullable=False, default="active", index=True)
    description = Column(String, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )

    pharmacy = relationship("Pharmacy")
    category = relationship("CatalogOption", foreign_keys=[category_id])


    @property
    def category_name(self):
        return self.category.name if self.category else None

    purchases = relationship(
        "PurchaseInvoice",
        back_populates="supplier",
    )