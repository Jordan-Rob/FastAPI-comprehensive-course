"""add column content to posts table

Revision ID: 49a35d5d1c0e
Revises: fb701833e826
Create Date: 2021-11-25 01:28:41.454784

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49a35d5d1c0e'
down_revision = 'fb701833e826'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'posts',
        sa.Column('content', sa.String(), nullable=False)
    )


def downgrade():
    op.drop_column(
        'posts',
        'content'
    )
