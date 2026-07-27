from sqlalchemy.orm import Session

from app.models.donation import Donation


class DonationRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, donation: Donation) -> Donation:
        self.db.add(donation)
        self.db.commit()
        self.db.refresh(donation)
        return donation

    def get_by_id(self, donation_id: int) -> Donation | None:
        return (
            self.db.query(Donation)
            .filter(Donation.id == donation_id)
            .first()
        )

    def get_by_payment_id(self, payment_id: str) -> Donation | None:
        return (
            self.db.query(Donation)
            .filter(Donation.payment_id == payment_id)
            .first()
        )
    
    def update(self, donation: Donation) -> Donation:
        self.db.add(donation)
        self.db.commit()
        self.db.refresh(donation)
        return donation