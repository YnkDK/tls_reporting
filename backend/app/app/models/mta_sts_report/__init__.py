from typing import List

from pydantic import BaseModel, Field, EmailStr

from app.models.mta_sts_report.mta_sts_datetime import MtaStsDatetime
from app.models.mta_sts_report.mta_sts_policy import PolicyContainer


class MtaStsReport(BaseModel):
    organization_name: str = Field(
        ...,
        description='The name of the organization responsible for the report.',
        example='Company-X',
        alias='organization-name'
    )
    date_range: MtaStsDatetime = Field(
        ...,
        description='The date-time indicates the start and end times for the report range.',
        alias='date-range'
    )
    contact_info: EmailStr = Field(
        ...,
        description='The contact information for the party responsible for the report.',
        alias='contact-info',
        example='sts-reporting@company-x.example'
    )
    report_id: str = Field(
        ...,
        description='A unique identifier for the report.  Report authors may use whatever scheme they prefer to '
                    'generate a unique identifier.',
        alias='report-id',
        example='5065427c-23d3-47ca-b6e0-946ea0e8c4be'
    )
    policies: List[PolicyContainer] = Field(
        ...,
        description='List of all policies the report covers.'
    )
