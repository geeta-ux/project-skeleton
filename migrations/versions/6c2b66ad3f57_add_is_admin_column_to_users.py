"""Add is_admin column to users

Revision ID: 6c2b66ad3f57
Revises: 68ddb764dc7b
Create Date: 2025-11-04 16:23:25.479337

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '6c2b66ad3f57'
down_revision: Union[str, Sequence[str], None] = '68ddb764dc7b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=True, server_default=sa.false()))

def downgrade():
    op.drop_column('users', 'is_admin')