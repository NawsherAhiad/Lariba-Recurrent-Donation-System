"""rename payment status success to completed

Revision ID: 70fd8ec5259b
Revises: c136434fa778
Create Date: 2026-06-28 22:59:57.579335

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '70fd8ec5259b'
down_revision: Union[str, Sequence[str], None] = 'c136434fa778'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute(
        "ALTER TYPE paymentstatus RENAME VALUE 'success' TO 'completed';"
    )


def downgrade():
    op.execute(
        "ALTER TYPE paymentstatus RENAME VALUE 'completed' TO 'success';"
    )