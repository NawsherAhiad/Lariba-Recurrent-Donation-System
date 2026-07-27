from decimal import Decimal

from pydantic import BaseModel


class CreatePaymentRequest(BaseModel):
    amount: Decimal
    intent: str = "sale"
    currency: str = "BDT"
    merchantInvoiceNumber: str


class ExecutePaymentRequest(BaseModel):
    paymentID: str