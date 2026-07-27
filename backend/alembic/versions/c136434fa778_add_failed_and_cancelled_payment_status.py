"""add failed and cancelled payment status

Revision ID: c136434fa778
Revises: 75f7c04efe4c
"""

from typing import Sequence, Union

from alembic import op

# revision identifiers
revision: str = "c136434fa778"
down_revision: Union[str, Sequence[str], None] = "75f7c04efe4c"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        ALTER TYPE paymentstatus
        RENAME VALUE 'success' TO 'completed';
        """
    )


def downgrade():
    op.execute(
        """
        ALTER TYPE paymentstatus
        RENAME VALUE 'completed' TO 'success';
        """
    )