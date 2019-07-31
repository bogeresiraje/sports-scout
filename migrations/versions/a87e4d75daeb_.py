"""empty message

Revision ID: a87e4d75daeb
Revises: 68731a6cfa06
Create Date: 2019-05-29 20:11:19.391466

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a87e4d75daeb'
down_revision = '68731a6cfa06'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('club', 'num_matches')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('club', sa.Column('num_matches', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
