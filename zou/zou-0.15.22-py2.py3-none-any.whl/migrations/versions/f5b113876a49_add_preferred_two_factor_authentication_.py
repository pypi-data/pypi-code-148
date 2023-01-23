"""Add preferred_two_factor_authentication for Person

Revision ID: f5b113876a49
Revises: 96c79d31e648
Create Date: 2022-12-01 15:58:36.117269

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = "f5b113876a49"
down_revision = "96c79d31e648"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "person",
        sa.Column(
            "preferred_two_factor_authentication",
            sa.String(length=30),
            nullable=True,
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("person", "preferred_two_factor_authentication")
    # ### end Alembic commands ###
