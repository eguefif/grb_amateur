"""add_user_table

Revision ID: 5c4410c1c914
Revises: 
Create Date: 2025-11-18 07:38:44.721640

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c4410c1c914'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
            'users',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('email', sa.String(75), nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
