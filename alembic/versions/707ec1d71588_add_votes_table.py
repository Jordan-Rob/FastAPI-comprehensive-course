"""add votes table

Revision ID: 707ec1d71588
Revises: ef71faaa3b9e
Create Date: 2021-11-25 02:25:01.703948

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '707ec1d71588'
down_revision = 'ef71faaa3b9e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('votes')
    # ### end Alembic commands ###
