from decimal import Decimal


from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.enums import PaymentMethod, PaymentStatus
from app.models.base import Base, TimestampMixin

from app.core.constants import (
    MAX_EMAIL_LENGTH,
    MAX_NAME_LENGTH,
    MAX_PHONE_LENGTH,
)


class Donation(Base, TimestampMixin):
    __tablename__ = "donations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    name: Mapped[str] = mapped_column(String(MAX_NAME_LENGTH), nullable=False)

    email: Mapped[str] = mapped_column(String(MAX_EMAIL_LENGTH), nullable=False)

    phone: Mapped[str] = mapped_column(String(MAX_PHONE_LENGTH), nullable=False)

    amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    payment_method: Mapped[PaymentMethod] = mapped_column(
        SQLEnum(PaymentMethod),
        default=PaymentMethod.bkash,
        nullable=False,
    )

    payment_status: Mapped[PaymentStatus] = mapped_column(
        SQLEnum(PaymentStatus),
        default=PaymentStatus.pending,
        nullable=False,
    )

    payment_id: Mapped[str | None] = mapped_column(
        String(MAX_NAME_LENGTH),
        nullable=True,
    )

    trx_id: Mapped[str | None] = mapped_column(
        String(MAX_NAME_LENGTH),
        nullable=True,
    )