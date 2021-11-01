from typing import Union, BinaryIO
from fastapi import UploadFile

from app.core.mta_sts import MtaSts
from app.models.resource_created import ResourceCreated


async def create_mta_sts_report(raw_content: Union[BinaryIO, UploadFile]) -> ResourceCreated:
    """Creates a new MTA-STS report.

    :param raw_content: The raw non-parsed report.
    :return: Information about the newly created resource.
    """
    report = await MtaSts.parse(raw_content)
    return ResourceCreated()
