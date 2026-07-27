from app.payment.bkash.checkout.client import BkashClient
from app.payment.bkash.checkout.schemas import CreatePaymentRequest
from app.payment.bkash.checkout.constants import CREATE_PAYMENT


class BkashCheckoutService:

    def __init__(self):
        self.client = BkashClient()
        
    async def create_payment(
        self,
        amount: float,
        invoice: str,
    ) -> dict:

        request = CreatePaymentRequest(
        amount=amount,
        merchantInvoiceNumber=invoice,
        )

        payload = {
            "amount": f"{request.amount:.2f}",
            "currency": request.currency,
            "intent": request.intent,
            "merchantInvoiceNumber": request.merchantInvoiceNumber,
        }

        print("\n========== CHECKOUT CREATE PAYMENT ==========")
        print(payload)

        return await self.client.post(
            endpoint=CREATE_PAYMENT,
            payload=payload,
        )