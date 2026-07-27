"""fix created_at default"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '75f7c04efe4c'
down_revision: Union[str, Sequence[str], None] = "84bdbdcd2c48"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "donations",
        "created_at",
        existing_type=sa.DateTime(timezone=True),
        server_default=sa.text("now()"),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "donations",
        "created_at",
        existing_type=sa.DateTime(timezone=True),
        server_default=None,
        existing_nullable=False,
    )