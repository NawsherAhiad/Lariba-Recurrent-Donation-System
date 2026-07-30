from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.enums import PaymentStatus
from app.payment.bkash.tokenized.client import BkashClient
from app.payment.bkash.tokenized.schemas import CreatePaymentRequest
from app.repositories.donation_repository import DonationRepository
from app.payment.bkash.tokenized.constants import *

from fastapi.responses import RedirectResponse
import json


class BkashPaymentService:

    def __init__(self, db: Session):
        self.client = BkashClient()
        self.repository = DonationRepository(db)

    async def create_payment(
        self,
        amount,
        invoice: str,
    ) -> dict:

        request = CreatePaymentRequest(
            amount=amount,
            merchantInvoiceNumber=invoice,
        )

        data = {
            "mode": "0011",
            "payerReference": request.merchantInvoiceNumber,
            "callbackURL": settings.BKASH_CALLBACK_URL,
            "amount": str(request.amount),
            "currency": request.currency,
            "intent": request.intent,
            "merchantInvoiceNumber": request.merchantInvoiceNumber,
        }

        print("\n========== CREATE PAYMENT ==========")
        print(data)

        return await self.client.post(
            endpoint=CREATE_PAYMENT,
            payload=data,
        )

    async def execute_payment(
        self,
        payment_id: str,
    ) -> dict:

        data = {
            "paymentID": payment_id,
        }

        return await self.client.post(
            endpoint=EXECUTE_PAYMENT,
            payload=data,
        )

    async def handle_callback(
        self,
        payment_id: str,
        status: str,
    ):

        print("\n")
        print("=" * 70)
        print("CALLBACK RECEIVED")
        print("=" * 70)
        print("Payment ID :", payment_id)
        print("Status     :", status)

        donation = self.repository.get_by_payment_id(payment_id)

        print("Donation Found :", donation is not None)

        if donation is not None:
            print("Donation ID    :", donation.id)
            print("DB Status      :", donation.payment_status)

        if donation is None:
            print("Donation not found in database.")

            return RedirectResponse(
                url="/frontend/payment-result.html?status=failed",
                status_code=302,
            )

        # Customer cancelled
        if status == "cancel":

            print("Customer cancelled payment.")

            donation.payment_status = PaymentStatus.cancelled
            self.repository.update(donation)

            return RedirectResponse(
                url="/frontend/payment-result.html?status=cancelled",
                status_code=302,
            )

        # Payment failed
        if status == "failure":

            print("Payment failed.")

            donation.payment_status = PaymentStatus.failed
            self.repository.update(donation)

            return RedirectResponse(
                url="/frontend/payment-result.html?status=failed",
                status_code=302,
            )

        # Unknown callback
        if status != "success":

            print("Unknown callback status:", status)

            return RedirectResponse(
                url="/frontend/payment-result.html?status=unknown",
                status_code=302,
            )

        # Already completed
        if donation.payment_status == PaymentStatus.completed:

            print("Payment already completed.")

            return RedirectResponse(
                url=f"/frontend/payment-result.html?status=success&trxID={donation.trx_id}",
                status_code=302,
            )

        print("\nExecuting Execute Payment API...")

        try:

            result = await self.execute_payment(payment_id)

            print("\n========== EXECUTE PAYMENT RESPONSE ==========")
            print(json.dumps(result, indent=4))

        except Exception as e:

            print("Execute API failed.")
            print(str(e))

            print("Trying Query Payment...")

            result = await self.query_payment(payment_id)

            print("\n========== QUERY PAYMENT RESPONSE ==========")
            print(json.dumps(result, indent=4))


        status_code = result.get("statusCode")
        transaction_status = result.get("transactionStatus")


        if status_code != "0000":

            print("bKash returned an error.")

            return RedirectResponse(
                url="/frontend/payment-result.html?status=failed",
                status_code=302,
            )


        # Update database

        if transaction_status == "Completed":

            donation.payment_status = PaymentStatus.completed
            donation.trx_id = result.get("trxID")

            self.repository.update(donation)

            print("Donation updated successfully.")

            return RedirectResponse(
                url=f"/frontend/payment-result.html?status=success&trxID={donation.trx_id}&amount={result.get('amount')}",
                status_code=302,
            )


        elif transaction_status == "Initiated":

            donation.payment_status = PaymentStatus.pending
            self.repository.update(donation)

            return RedirectResponse(
                url="/frontend/payment-result.html?status=pending",
                status_code=302,
            )


        elif transaction_status in ("Cancelled", "Failed"):

            donation.payment_status = PaymentStatus.failed
            self.repository.update(donation)

            return RedirectResponse(
                url="/frontend/payment-result.html?status=failed",
                status_code=302,
            )


        else:

            return RedirectResponse(
                url="/frontend/payment-result.html?status=unknown",
                status_code=302,
            )


    async def query_payment(
        self,
        payment_id: str,
    ) -> dict:

        data = {
            "paymentID": payment_id,
        }

        print("\n========== QUERY PAYMENT ==========")
        print(data)

        result = await self.client.post(
            endpoint=QUERY_PAYMENT,
            payload=data,
        )

        print(json.dumps(result, indent=4))

        return result


    async def search_transaction(
        self,
        trx_id: str,
    ) -> dict:

        data = {
            "trxID": trx_id,
        }

        return await self.client.post(
            endpoint=SEARCH_TRANSACTION,
            payload=data,
        )