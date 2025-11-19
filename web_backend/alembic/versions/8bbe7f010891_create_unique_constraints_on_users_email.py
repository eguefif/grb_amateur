"""create unique constraints on users email

Revision ID: 8bbe7f010891
Revises: d3b25763c4c3
Create Date: 2025-11-19 21:39:48.864181

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8bbe7f010891'
down_revision: Union[str, Sequence[str], None] = 'd3b25763c4c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint('uq_user_email', "users", ["email"])


def downgrade() -> None:
    """Downgrade schema."""
    pass
