from enum import Enum


class PaymentMethod(str, Enum):
    bkash = "bkash"


# class PaymentStatus(str, Enum):
#     pending = "pending"
#     success = "success"
#     failed = "failed"
#     cancelled = "cancelled"

class PaymentStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"
    cancelled = "cancelled"