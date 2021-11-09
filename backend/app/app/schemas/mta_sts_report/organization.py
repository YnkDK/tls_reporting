from pydantic import BaseModel


class OrganisationBase(BaseModel):
    name: str


OrganisationCreate = OrganisationBase
OrganisationUpdate = OrganisationBase
