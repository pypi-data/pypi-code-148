"""add login_failed_attemps and last_login_failed column to person

Revision ID: a6c25eed3ea1
Revises: 82ee682204ab
Create Date: 2022-10-15 02:10:18.559767

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = "a6c25eed3ea1"
down_revision = "82ee682204ab"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "person",
        sa.Column("login_failed_attemps", sa.Integer(), nullable=True),
    )
    op.add_column(
        "person", sa.Column("last_login_failed", sa.DateTime(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("person", "last_login_failed")
    op.drop_column("person", "login_failed_attemps")
    # ### end Alembic commands ###
