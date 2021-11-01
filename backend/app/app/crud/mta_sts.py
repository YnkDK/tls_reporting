from app.models.mta_sts_report import MtaStsReport
from app.models.resource_created import ResourceCreated


async def create_mta_sts_report(mta_sts_report: MtaStsReport) -> ResourceCreated:
    """Creates a new MTA-STS report.

    :param mta_sts_report: The parsed report.
    :return: Information about the newly created resource.
    """
    return ResourceCreated()
