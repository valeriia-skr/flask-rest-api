"""empty message

Revision ID: 48f08e8426c5
Revises: ae6ed5f0e8a2
Create Date: 2023-09-24 09:51:26.779098

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48f08e8426c5'
down_revision = 'ae6ed5f0e8a2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=80),
               type_=sa.String(length=256),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.String(length=256),
               type_=sa.VARCHAR(length=80),
               existing_nullable=False)
    # ### end Alembic commands ###
