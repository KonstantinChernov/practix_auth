"""fix

Revision ID: 6eeb7fbffbd8
Revises: af17df2d7da1
Create Date: 2021-11-28 23:39:01.972873

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6eeb7fbffbd8'
down_revision = 'af17df2d7da1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('social_account',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('social_id', sa.Text(), nullable=False),
    sa.Column('social_name', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('social_id', 'social_name', name='social_pk')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('social_account')
    # ### end Alembic commands ###
