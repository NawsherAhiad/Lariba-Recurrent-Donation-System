from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.donation import DonationCreate
from app.schemas.response import ApiResponse
from app.services.donation_service import DonationService

router = APIRouter()


@router.post(
    "/donations",
    response_model=ApiResponse,
)
async def create_donation(
    payload: DonationCreate,
    db: Session = Depends(get_db),
):
    result = await DonationService(db).create(payload)
    
    donation = result["donation"]
    payment = result["payment"]
    
    return ApiResponse(
        success=True,
        message="Donation created successfully.",
        data={
            "id": donation.id,
            "name": donation.name,
            "email": donation.email,
            "phone": donation.phone,
            "amount": str(donation.amount),
            "payment_status": donation.payment_status.value,
            "payment_method": donation.payment_method.value,

            "payment_id": payment["paymentID"],
            "bkash_url": payment["bkashURL"],
        }
    )