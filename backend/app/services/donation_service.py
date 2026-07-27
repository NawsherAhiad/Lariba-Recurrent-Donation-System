from decimal import Decimal

from sqlalchemy.orm import Session

from app.core.enums import PaymentMethod, PaymentStatus
from app.models.donation import Donation
from app.repositories.donation_repository import DonationRepository
from app.schemas.donation import DonationCreate
from app.payment.bkash.tokenized.service import BkashPaymentService

class DonationService:

    def __init__(self, db: Session):
        self.repository = DonationRepository(db)
        self.payment_service = BkashPaymentService(db)

    async def create(self, payload: DonationCreate) -> dict[str, object]:

        donation = Donation(
            name=payload.name,
            email=payload.email,
            phone=payload.phone,
            amount=Decimal(payload.amount),
            payment_method=PaymentMethod.bkash,
            payment_status=PaymentStatus.pending,
        )

        #return self.repository.create(donation)
        donation = self.repository.create(donation)
        invoice = f"DON-{donation.id}"
        
        payment = await self.payment_service.create_payment(
            amount=donation.amount,
            invoice=invoice,
        )
        print(payment)
        
        donation.payment_id = payment["paymentID"]
        self.repository.update(donation)
        # return donation
        return {
            "donation": donation,
            "payment": payment,
        }