"""add last columns to posts table

Revision ID: ef71faaa3b9e
Revises: ab9edfbd85cf
Create Date: 2021-11-25 02:04:23.325599

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef71faaa3b9e'
down_revision = 'ab9edfbd85cf'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'posts', sa.Column('published', sa.Boolean(), server_default='TRUE', nullable=False)
    )
    op.add_column(
        'posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
    )


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
