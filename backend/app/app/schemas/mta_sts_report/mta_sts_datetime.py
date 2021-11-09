import datetime

from pydantic import BaseModel, Field


class MtaStsDatetime(BaseModel):
    start_datetime: datetime.datetime = Field(
        ...,
        title="The start time for the report range.",
        alias="start-datetime",
        example=datetime.datetime(2016, 4, 1, tzinfo=datetime.timezone.utc),
    )
    end_datetime: datetime.datetime = Field(
        ...,
        title="The end time for the report range.",
        alias="end-datetime",
        example=datetime.datetime(2016, 4, 1, 23, 59, 59, tzinfo=datetime.timezone.utc),
    )
