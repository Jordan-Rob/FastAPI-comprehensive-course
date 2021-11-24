"""add foreign key to posts table

Revision ID: ab9edfbd85cf
Revises: 8a5297c1ebcf
Create Date: 2021-11-25 01:54:24.653077

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab9edfbd85cf'
down_revision = '8a5297c1ebcf'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users',
        local_cols=['user_id'], remote_cols=['id'], ondelete="CASCADE"
    )


def downgrade():
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'user_id')