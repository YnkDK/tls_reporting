import datetime
from typing import List, Text

from app.crud.base import CRUDBase
from app.db.base_class import Base
from app.schemas.mta_sts_report.mta_sts_policy import PolicyTypes
from app.schemas.mta_sts_report.organization import (
    OrganisationCreate,
    OrganisationUpdate,
)
from pydantic import EmailStr
from sqlalchemy import ARRAY, VARCHAR, Column, DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Session, relationship


class Policy(Base):
    __tablename__ = "Policies"
    policy_id: str = Column("PolicyID", String(length=25), primary_key=True)
    policy_type: PolicyTypes = Column("PolicyType", Enum(PolicyTypes), nullable=False)
    policy_string: List[str] = Column("PolicyString", ARRAY(str), nullable=False)
    policy_domain: str = Column("PolicyDomain", VARCHAR(255), nullable=False)
    mx_host: str = Column("MxHost", VARCHAR(450), nullable=True)

    report_id = Column(
        "ReportID",
        String(length=25),
        ForeignKey("Policies.PolicyID"),
        nullable=False,
    )
    organisation = relationship("Organisation")


class CRUDPolicy(CRUDBase[Policy, OrganisationCreate, OrganisationUpdate]):
    pass


policies = CRUDPolicy(Policy)
