"""seed users table in grb.db

Revision ID: d3b25763c4c3
Revises: 5c4410c1c914
Create Date: 2025-11-19 07:50:08.499333

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from seed import seed


# revision identifiers, used by Alembic.
revision: str = 'd3b25763c4c3'
down_revision: Union[str, Sequence[str], None] = '5c4410c1c914'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    users_table = sa.table('users',
        sa.column('id', sa.Integer),
        sa.column('email', sa.String)
    )

    # Generate fake users data
    users_data = seed.generate_users(4)

    # Use Alembic's connection context to insert data
    op.bulk_insert(users_table, users_data)


def downgrade() -> None:
    """Downgrade schema."""
    # Delete all users from the table
    op.execute("DELETE FROM users")
