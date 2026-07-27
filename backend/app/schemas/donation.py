from decimal import Decimal
import re

from pydantic import BaseModel, EmailStr, field_validator


PHONE_REGEX = re.compile(r"^(?:\+88|88)?01[3-9]\d{8}$")


class DonationCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    amount: Decimal

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        if not PHONE_REGEX.fullmatch(value):
            raise ValueError("Invalid Bangladeshi phone number.")
        return value

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, value: Decimal) -> Decimal:
        if value < Decimal("10"):
            raise ValueError("Minimum donation amount is 10 BDT.")
        return value