"""Create report table

Revision ID: d7efad102a8a
Revises: ba9997532100
Create Date: 2021-11-09 12:38:31.586844

"""
import sqlalchemy as sa
from app.db.utils import UtcNow

# revision identifiers, used by Alembic.
from sqlalchemy import VARCHAR, DateTime

from alembic import op

revision = "d7efad102a8a"
down_revision = "ba9997532100"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "Reports",
        sa.Column("ReportID", sa.String(length=64), primary_key=True),
        sa.Column("StartDatetime", DateTime, nullable=False),
        sa.Column("EndDatetime", DateTime, nullable=False),
        sa.Column("ContactInfo", VARCHAR(64 + 1 + 255), nullable=False),
        sa.Column("ExternalID", VARCHAR(255), nullable=False, doc="Original report-id"),
        sa.Column(
            "OrganisationID",
            sa.String(length=25),
            sa.ForeignKey("Organisations.OrganisationID"),
            nullable=False,
        ),
        sa.Column("Created", sa.DateTime(), nullable=False, server_default=UtcNow()),
        sa.Column(
            "Updated",
            sa.DateTime(),
            nullable=False,
            server_default=UtcNow(),
            onupdate=UtcNow(),
        ),
        sa.PrimaryKeyConstraint("ReportID"),
        sa.Index(
            "UX_Reports_ExternalID_OrganisationID",
            "ExternalID",
            "OrganisationID",
            unique=True,
        ),
    )


def downgrade():
    op.drop_table("Reports")
