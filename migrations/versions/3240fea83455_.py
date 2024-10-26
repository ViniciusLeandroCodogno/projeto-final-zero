"""empty message

Revision ID: 3240fea83455
Revises: 819f9f2bb08f
Create Date: 2024-10-26 16:03:44.703183

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3240fea83455'
down_revision = '819f9f2bb08f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('data_criacao', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('data_criacao')

    # ### end Alembic commands ###
