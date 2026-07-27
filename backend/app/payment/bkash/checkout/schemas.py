from pydantic import BaseModel


class CreatePaymentRequest(BaseModel):
    amount: float
    merchantInvoiceNumber: str
    currency: str = "BDT"
    intent: str = "sale"