from fastapi import HTTPException, status

class FinancialException(HTTPException):
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail=detail)

class DuplicateTransactionError(FinancialException):
    def __init__(self, txn_id: str):
        super().__init__(
            detail=f"Transaction with ID '{txn_id}' has already been processed.",
            status_code=status.HTTP_409_CONFLICT
        )

class InvalidSignatureError(FinancialException):
    def __init__(self, gateway: str):
        super().__init__(
            detail=f"Signature verification failed for gateway '{gateway}'.",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

class InsufficientBalanceError(FinancialException):
    def __init__(self):
        super().__init__(
            detail="Debit transaction rejected: Insufficient ledger balance.",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )