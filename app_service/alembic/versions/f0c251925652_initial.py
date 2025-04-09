"""Initial

Revision ID: f0c251925652
Revises: 
Create Date: 2025-04-09 03:37:03.718900

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f0c251925652'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('create extension if not exists "uuid-ossp";')
    op.create_table('requests',
    sa.Column('id', sa.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('address', sa.VARCHAR(length=42), nullable=False),
    sa.Column('bandwidth', sa.BigInteger(), nullable=False),
    sa.Column('energy', sa.BigInteger(), nullable=False),
    sa.Column('trx_balance', sa.Numeric(precision=30, scale=6), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_requests')),
    schema='public'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('requests', schema='public')
    op.execute('drop extension if exists "uuid-ossp";')
    # ### end Alembic commands ###
