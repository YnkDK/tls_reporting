import datetime

from app.crud.base import CRUDBase
from app.db.base_class import Base
from app.schemas.mta_sts_report.organization import (
    OrganisationCreate,
    OrganisationUpdate,
)
from pydantic import EmailStr
from sqlalchemy import VARCHAR, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import Session, relationship


class Report(Base):
    __tablename__ = "Reports"
    report_id: str = Column("ReportID", String(length=25), primary_key=True)
    start_datetime: datetime.datetime = Column(
        "StartDatetime", DateTime, nullable=False
    )
    end_datetime: datetime.datetime = Column("EndDatetime", DateTime, nullable=False)
    # RFC3696#section-3
    # That limit is a maximum of 64 characters (octets) in the "local part" (before the "@") and
    # a maximum of 255 characters (octets) in the domain part (after the "@")
    contact_info: EmailStr = Column(
        "ContactInfo", VARCHAR(64 + 1 + 255), nullable=False
    )
    external_id: str = Column(
        "ExternalID", VARCHAR(255), nullable=False, doc="Original report-id"
    )

    organisation_id = Column(
        "OrganisationID",
        String(length=25),
        ForeignKey("Organisations.OrganisationID"),
        nullable=False,
    )
    organisation = relationship("Organisation")


class CRUDReport(CRUDBase[Report, OrganisationCreate, OrganisationUpdate]):
    def get_id(self, db: Session, *, external_id: str, organisation_id: str) -> str:
        result = (
            db.query(self.model)
            .filter(
                Report.external_id == external_id,
                Report.organisation_id == organisation_id,
            )
            .with_entities(Report.report_id)
            .one()
        )
        return result[0]


reports = CRUDReport(Report)
