from sqlalchemy.orm import declarative_base
import enum

Base = declarative_base()

class TransactionType(str, enum.Enum):
    CREDIT = "credit"
    DEBIT = "debit"