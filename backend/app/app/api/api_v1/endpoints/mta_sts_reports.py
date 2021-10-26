from fastapi import APIRouter, UploadFile, File, status, Response, Request
from urllib.parse import urljoin

from app.core import http_headers
from app.models.resource_created import ResourceCreated
from app.crud import mta_sts

router = APIRouter()


@router.post(
    '/mta-sts',
    response_model=ResourceCreated,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            'headers': {
                http_headers.LOCATION: {'description': 'The location of the newly created resource.', 'type': 'string'}
            }
        }
    }
)
async def create_mta_sts_report(
        response: Response,
        request: Request,
        report: UploadFile = File(
            ...,
            title='The MTA-STS report to be handled',
            description='Plaintext file encoded in the Internet JSON (I-JSON) format (might be gzipped)'
        )):
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

    Parses a new MTA-STS report in either plain text or encoded in gz format."""
    result = await mta_sts.create_mta_sts_report(report.filename, report)

    response.headers['Location'] = urljoin(str(request.url) + '/', result.identifier)
    return result
