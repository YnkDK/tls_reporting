from typing import Union, BinaryIO
from fastapi import UploadFile

from app.core.mta_sts import MtaSts
from app.models.resource_created import ResourceCreated


async def create_mta_sts_report(report_name: str, raw_content: Union[BinaryIO, UploadFile]) -> ResourceCreated:
    """Creates a new MTA-STS report.

    :param report_name: The name of the report.
    :param raw_content: The raw non-parsed report.
    :return: Information about the newly created resource.
    """
    mta_sts = MtaSts(report_name)
    await mta_sts.parse(raw_content)
    return ResourceCreated()
