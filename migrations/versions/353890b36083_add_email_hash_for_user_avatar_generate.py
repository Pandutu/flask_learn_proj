"""add email hash for user avatar generate"

Revision ID: 353890b36083
Revises: ea7e4ff1c291
Create Date: 2017-08-01 02:22:19.734709

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '353890b36083'
down_revision = 'ea7e4ff1c291'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('avatar_hash', sa.String(length=32), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'avatar_hash')
    # ### end Alembic commands ###
