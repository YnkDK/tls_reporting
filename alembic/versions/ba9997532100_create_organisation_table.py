"""Create organisation table

Revision ID: ba9997532100
Revises:
Create Date: 2021-11-08 14:36:59.635469

"""
import sqlalchemy as sa

# revision identifiers, used by Alembic.
from app.db.utils import UtcNow

from alembic import op

revision = "ba9997532100"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "Organisations",
        sa.Column("OrganisationID", sa.String(length=64), primary_key=True),
        sa.Column("Name", sa.VARCHAR(255), index=True, nullable=False, unique=True),
        sa.Column("Created", sa.DateTime(), nullable=False, server_default=UtcNow()),
        sa.Column(
            "Updated",
            sa.DateTime(),
            nullable=False,
            server_default=UtcNow(),
            onupdate=UtcNow(),
        ),
        sa.PrimaryKeyConstraint("OrganisationID"),
    )


def downgrade():
    op.drop_table("Organisations")
