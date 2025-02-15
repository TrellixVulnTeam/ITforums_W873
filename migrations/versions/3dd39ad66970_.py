"""empty message

Revision ID: 3dd39ad66970
Revises: 2eb584575727
Create Date: 2018-12-10 13:08:17.846006

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3dd39ad66970'
down_revision = '2eb584575727'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Post', sa.Column('author_id', sa.String(length=64), nullable=True))
    op.create_foreign_key(None, 'Post', 'front_user', ['author_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Post', type_='foreignkey')
    op.drop_column('Post', 'author_id')
    # ### end Alembic commands ###
