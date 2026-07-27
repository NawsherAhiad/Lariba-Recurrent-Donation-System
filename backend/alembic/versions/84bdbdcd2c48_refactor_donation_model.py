"""refactor donation model

Revision ID: 84bdbdcd2c48
Revises: c387ab049ac0
Create Date: 2026-06-27 23:04:58.205362

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '84bdbdcd2c48'
down_revision: Union[str, Sequence[str], None] = 'c387ab049ac0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    payment_method = sa.Enum(
        "bkash",
        name="paymentmethod",
    )

    payment_status = sa.Enum(
        "pending",
        "success",
        "failed",
        "cancelled",
        name="paymentstatus",
    )

    payment_method.create(op.get_bind(), checkfirst=True)
    payment_status.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "donations",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )

    op.alter_column(
        "donations",
        "payment_method",
        existing_type=sa.VARCHAR(length=20),
        type_=payment_method,
        existing_nullable=False,
        postgresql_using="payment_method::paymentmethod",
    )

    op.alter_column(
        "donations",
        "payment_status",
        existing_type=sa.VARCHAR(length=20),
        type_=payment_status,
        existing_nullable=False,
        postgresql_using="payment_status::paymentstatus",
    )

    op.alter_column(
        "donations",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.alter_column(
        "donations",
        "created_at",
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
    )

    op.alter_column(
        "donations",
        "payment_status",
        existing_type=sa.Enum(
            "pending",
            "success",
            "failed",
            "cancelled",
            name="paymentstatus",
        ),
        type_=sa.VARCHAR(length=20),
        existing_nullable=False,
        postgresql_using="payment_status::text",
    )

    op.alter_column(
        "donations",
        "payment_method",
        existing_type=sa.Enum(
            "bkash",
            name="paymentmethod",
        ),
        type_=sa.VARCHAR(length=20),
        existing_nullable=False,
        postgresql_using="payment_method::text",
    )

    op.drop_column("donations", "updated_at")

    sa.Enum(
        "pending",
        "success",
        "failed",
        "cancelled",
        name="paymentstatus",
    ).drop(op.get_bind(), checkfirst=True)

    sa.Enum(
        "bkash",
        name="paymentmethod",
    ).drop(op.get_bind(), checkfirst=True)