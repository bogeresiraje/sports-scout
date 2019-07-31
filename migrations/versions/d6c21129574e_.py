"""empty message

Revision ID: d6c21129574e
Revises: 89ed93ac40ea
Create Date: 2019-05-30 01:17:21.102515

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd6c21129574e'
down_revision = '89ed93ac40ea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('manager_username_key', 'manager', type_='unique')
    op.drop_column('manager', 'username')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('manager', sa.Column('username', sa.VARCHAR(length=100), autoincrement=False, nullable=False))
    op.create_unique_constraint('manager_username_key', 'manager', ['username'])
    # ### end Alembic commands ###
