"""create users table

Revision ID: 8a5297c1ebcf
Revises: 49a35d5d1c0e
Create Date: 2021-11-25 01:37:00.090150

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a5297c1ebcf'
down_revision = '49a35d5d1c0e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users', 
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
            server_default=sa.text('now()'),nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    


def downgrade():
    op.drop_table('users')
