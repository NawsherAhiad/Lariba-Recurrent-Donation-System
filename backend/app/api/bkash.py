from decimal import Decimal

from fastapi import APIRouter, Query

from app.payment.bkash.tokenized.auth import BkashAuth
from app.payment.bkash.tokenized.schemas import CreatePaymentRequest
from app.payment.bkash.tokenized.service import BkashPaymentService

from app.payment.bkash.checkout.service import BkashCheckoutService

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.database import get_db

router = APIRouter(
    prefix="/bkash",
    tags=["bKash"],
)

checkout_service = BkashCheckoutService()
@router.post("/checkout/test")
async def checkout_test():

    result = await checkout_service.create_payment(
        amount=100,
        invoice="TEST-1001",
    )

    return result
# @router.get("/token")
# async def get_token():
#     auth = BkashAuth()
#     return await auth.grant_token()


# @router.post("/create-payment")
# async def create_payment():

#     service = BkashPaymentService()

#     payload = CreatePaymentRequest(
#         amount=Decimal("100"),
#         merchantInvoiceNumber="INV-10001",
#     )

#     return await service.create_payment(payload)
@router.get("/test-auth")
async def test_auth():
    auth = BkashAuth()
    return await auth.grant_token()

@router.get("/test-payment")
async def test_payment(
    db: Session = Depends(get_db),
):
    service = BkashPaymentService(db)

    return await service.create_payment(
        amount=100,
        invoice="TEST-001",
    )


@router.get("/callback")
async def callback(
    paymentID: str = Query(...),
    status: str = Query(...),
    db: Session = Depends(get_db),
):
    print("===== BKASH CALLBACK =====")
    print(dict(request.query_params))
    print("==========================")
    
    service = BkashPaymentService(db)

    return await service.handle_callback(
        payment_id=paymentID,
        status=status,
    )
    

@router.get("/search/{trx_id}")
async def search_transaction(
    trx_id: str,
    db: Session = Depends(get_db),
):
    service = BkashPaymentService(db)
    return await service.search_transaction(trx_id)