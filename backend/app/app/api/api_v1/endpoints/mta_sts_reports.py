from urllib.parse import urljoin

from app.api import deps
from app.core import exceptions, http_headers
from app.core.mta_sts import MtaSts
from app.crud import mta_sts
from app.schemas import IDENTIFIER_INFORMATION
from app.schemas.http_exception import HttpException
from app.schemas.mta_sts_report import MtaStsReport
from app.schemas.resource_created import ResourceCreated
from fastapi import (
    APIRouter,
    Depends,
    File,
    Path,
    Request,
    Response,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

router = APIRouter()


@router.post(
    "/mta-sts",
    operation_id="create_mta_sts_report",
    status_code=status.HTTP_201_CREATED,
    response_model=ResourceCreated,
    response_description="The report has been successfully processed and a new entity has been created.",
    responses={
        status.HTTP_201_CREATED: {
            "headers": {
                http_headers.LOCATION: {
                    "description": "The location of the newly created resource.",
                    "schema": {"type": "string"},
                }
            },
            "content": {
                "application/json": {"examples": ResourceCreated.openapi_examples()}
            },
            "links": {
                "Get MTA-STS Report": {
                    "operationId": "get_mta_sts_report",
                    "parameters": {
                        "identifier": "$response.body#/identifier",
                    },
                    "description": "The `identifier` value returned in the response can be used as the `identifier`"
                    " parameter in `GET /mta-sts/{identifier}`",
                }
            },
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": HttpException,
            "description": "The report could not be processed.",
            "content": {
                "application/json": {
                    "examples": exceptions.openapi_examples(
                        frozenset(
                            {
                                exceptions.JsonError.ERROR_CODE,
                                exceptions.GzipError.ERROR_CODE,
                                exceptions.ResourceAlreadyExists.ERROR_CODE,
                            }
                        )
                    )
                }
            },
        },
    },
)
async def create_mta_sts_report(
    response: Response,
    request: Request,
    db: Session = Depends(deps.get_db),
    report: UploadFile = File(
        ...,
        title="The MTA-STS report to be handled",
        description="Plaintext file encoded in the Internet JSON (I-JSON) format (might be gzipped)",
    ),
):
    """The report is composed as a plaintext file encoded in the Internet JSON (I-JSON) format [RFC7493].

    Aggregate reports contain the following fields:
    1. Report metadata:
        - The organization responsible for the report
        - Contact information for one or more responsible parties for the contents of the report
        -  A unique identifier for the report
        -  The reporting date range for the report
    2. Policy, consisting of:
        - One of the following policy types:
            (1) the MTA-STS Policy applied (as a string),
            (2) the DANE TLSA record applied (as a string, with each RR entry of the RR set listed and separated by a
            semicolon),
            (3) the literal string "no-policy-found", if neither a DANE nor MTA-STS Policy could be found.
        - The domain for which the policy is applied
        - The MX host
    3. Aggregate counts, comprising result type, Sending MTA IP, receiving MTA hostname, session count, and an optional
    additional information field containing a URI for recipients to review further information on a failure type.

    Processes a new MTA-STS report in either plain text or encoded in gz format."""
    mta_sts_report = await MtaSts.parse(report)

    try:
        result = await mta_sts.create_mta_sts_report(
            db=db, mta_sts_report=mta_sts_report
        )
    except Exception:
        db.rollback()
        raise

    response.headers["Location"] = urljoin(str(request.url) + "/", result.identifier)
    return result


@router.get(
    "/mta-sts/{identifier}",
    operation_id="get_mta_sts_report",
    response_model=MtaStsReport,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": HttpException,
            "content": {
                "application/json": {
                    "examples": exceptions.openapi_examples(
                        frozenset({exceptions.ResourceNotFound.ERROR_CODE})
                    )
                }
            },
        }
    },
)
async def get_mta_sts_report(identifier: str = Path(..., **IDENTIFIER_INFORMATION)):
    """Retrieves a given MTA-STS report."""
    raise exceptions.ResourceNotFound(NotImplementedError(identifier))
