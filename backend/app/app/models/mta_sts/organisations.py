from app.crud.base import CRUDBase
from app.db.base_class import Base
from app.schemas.mta_sts_report.organization import (
    OrganisationCreate,
    OrganisationUpdate,
)
from app.schemas.resource_created import ResourceCreated
from sqlalchemy import VARCHAR, Column, String
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session


class Organisation(Base):
    __tablename__ = "Organisations"
    organisation_id: str = Column("OrganisationID", String(length=25), primary_key=True)
    name: str = Column("Name", VARCHAR(255), index=True, nullable=False, unique=True)


class CRUDOrganisation(CRUDBase[Organisation, OrganisationCreate, OrganisationUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Organisation:
        return db.query(self.model).filter(Organisation.name == name).one()

    def upsert(self, db: Session, *, name: str) -> ResourceCreated:
        try:
            org = self.get_by_name(db, name=name)
            return ResourceCreated(identifier=org.organisation_id)
        except NoResultFound:
            return self.create(db, obj_in=OrganisationCreate(name=name))


organisations = CRUDOrganisation(Organisation)
