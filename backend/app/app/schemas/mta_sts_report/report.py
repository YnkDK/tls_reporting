import datetime

from pydantic import BaseModel, EmailStr, Field

from .. import IDENTIFIER_INFORMATION
from . import MtaStsReport
from .mta_sts_datetime import MtaStsDatetime


class ReportBase(BaseModel):
    start_datetime: datetime.datetime
    end_datetime: datetime.datetime
    contact_info: EmailStr
    external_id: str
    organisation_id: str


ReportCreate = ReportBase
ReportUpdate = ReportBase
