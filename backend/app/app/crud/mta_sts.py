from typing import Union

from app.core.exceptions import ResourceAlreadyExists
from app.models.mta_sts import organisations, reports
from app.schemas.mta_sts_report import MtaStsReport
from app.schemas.mta_sts_report.report import ReportCreate
from app.schemas.resource_created import ResourceCreated
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


def _prepare_resource_already_exists_or_keep_original(
    db: Session,
    original_exception: IntegrityError,
    external_id: str,
    organisation_id: str,
) -> Union[ResourceAlreadyExists, IntegrityError]:
    if (
        len(original_exception.args) == 1
        and original_exception.args[0]
        == "(sqlite3.IntegrityError) UNIQUE constraint failed: Reports.ExternalID, Reports.OrganisationID"
    ):
        db.rollback()
        existing_identifier = reports.get_id(
            db,
            external_id=external_id,
            organisation_id=organisation_id,
        )
        return ResourceAlreadyExists(original_exception, existing_identifier)
    return original_exception


async def create_mta_sts_report(
    db: Session, mta_sts_report: MtaStsReport
) -> ResourceCreated:
    """Creates a new MTA-STS report.

    :param db: The active database session.
    :param mta_sts_report: The parsed report.
    :return: Information about the newly created resource.
    """

    organisation_identifier = organisations.upsert(
        db, name=mta_sts_report.organization_name
    ).identifier

    try:
        report_identifier = reports.create(
            db,
            obj_in=ReportCreate(
                start_datetime=mta_sts_report.date_range.start_datetime,
                end_datetime=mta_sts_report.date_range.end_datetime,
                contact_info=mta_sts_report.contact_info,
                external_id=mta_sts_report.report_id,
                organisation_id=organisation_identifier,
            ),
        )
    except IntegrityError as e:
        raise _prepare_resource_already_exists_or_keep_original(
            db, e, mta_sts_report.report_id, organisation_identifier
        )

    for policy in mta_sts_report.policies:
        print(policy)

    return report_identifier
