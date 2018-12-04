"""empty message

Revision ID: 9a9bdbbd784b
Revises: 44fac7dc74ee
Create Date: 2018-12-04 15:06:48.304646

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a9bdbbd784b'
down_revision = '44fac7dc74ee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Carousel',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.Column('pictureurl', sa.String(length=256), nullable=False),
    sa.Column('nexturl', sa.String(length=256), nullable=False),
    sa.Column('weight', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Carousel')
    # ### end Alembic commands ###
