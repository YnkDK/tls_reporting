from typing import Any, List, Optional

from app.schemas import IDENTIFIER_INFORMATION
from fastapi import HTTPException, status
from pydantic import ValidationError


class TLSReportingExceptionBase(HTTPException):
    STATUS_CODE = 0
    MESSAGE = ""
    ERROR_CODE = ""
    _ADDITIONAL_EXAMPLE: Optional[List[Any]] = None

    def __init__(
        self,
        original_exception: Exception,
        message: str,
        error_code: str,
        http_status_code: int,
        additional: Optional[List[Any]] = None,
    ):
        if additional:
            detail = {"message": message, "code": error_code, "additional": additional}
        else:
            detail = {"message": message, "code": error_code}

        super().__init__(status_code=http_status_code, detail=detail)
        self.original_exception = original_exception

    @classmethod
    def additional_example(cls) -> Optional[List[Any]]:
        return cls._ADDITIONAL_EXAMPLE


class ResourceNotFound(TLSReportingExceptionBase):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    MESSAGE = "Indicates that the resource is missing: not whether the absence is temporary or permanent."
    ERROR_CODE = "404-01"

    def __init__(self, original_exception: Exception):
        super().__init__(
            original_exception=original_exception,
            message=ResourceNotFound.MESSAGE,
            error_code=ResourceNotFound.ERROR_CODE,
            http_status_code=ResourceNotFound.STATUS_CODE,
        )


class ResourceAlreadyExists(TLSReportingExceptionBase):
    STATUS_CODE = status.HTTP_409_CONFLICT
    MESSAGE = "Indicates that the resource already exists. See additional field for the identifier of the resource."
    ERROR_CODE = "409-01"
    _ADDITIONAL_EXAMPLE = [IDENTIFIER_INFORMATION.get("example")]

    def __init__(self, original_exception: Exception, existing_identifier: str):
        super().__init__(
            original_exception=original_exception,
            message=ResourceAlreadyExists.MESSAGE,
            error_code=ResourceAlreadyExists.ERROR_CODE,
            http_status_code=ResourceAlreadyExists.STATUS_CODE,
            additional=[existing_identifier],
        )


class GzipError(TLSReportingExceptionBase):
    STATUS_CODE = status.HTTP_422_UNPROCESSABLE_ENTITY
    MESSAGE = "An error occurred during encoding/decoding the content to/from Gzip."
    ERROR_CODE = "422-01"

    def __init__(self, original_exception: Exception):
        super().__init__(
            original_exception=original_exception,
            message=GzipError.MESSAGE,
            error_code=GzipError.ERROR_CODE,
            http_status_code=GzipError.STATUS_CODE,
        )


class JsonError(TLSReportingExceptionBase):
    STATUS_CODE = status.HTTP_422_UNPROCESSABLE_ENTITY
    MESSAGE = "An error occurred while parsing the JSON content, e.g., not well formatted or incorrect types."
    ERROR_CODE = "422-02"
    _ADDITIONAL_EXAMPLE = [
        {
            "loc": ["policies", 0, "policy", "policy-type"],
            "msg": "field required",
            "type": "value_error.missing",
        },
        {
            "loc": ["policies", 0, "policy", "policy-string"],
            "msg": "field required",
            "type": "value_error.missing",
        },
    ]

    def __init__(self, original_exception: Exception):
        additional = None
        if isinstance(original_exception, ValidationError):
            additional = original_exception.errors()
        super().__init__(
            original_exception=original_exception,
            message=JsonError.MESSAGE,
            error_code=JsonError.ERROR_CODE,
            http_status_code=JsonError.STATUS_CODE,
            additional=additional,
        )


class InternalServerError(TLSReportingExceptionBase):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    MESSAGE = "The server encountered an unexpected condition that prevented it from fulfilling the request."
    ERROR_CODE = "500-01"

    def __init__(self, original_exception: Exception):
        super().__init__(
            original_exception=original_exception,
            message=InternalServerError.MESSAGE,
            error_code=InternalServerError.ERROR_CODE,
            http_status_code=InternalServerError.STATUS_CODE,
        )


def openapi_examples(error_codes: frozenset = None) -> dict:
    """Generates a list of all or a subset of all errors to be used in OpenAPI documentation.

    If error_codes is provided only the error codes

    """
    all_exceptions = dict()
    for subclass in TLSReportingExceptionBase.__subclasses__():
        if error_codes is None or subclass.ERROR_CODE in error_codes:
            all_exceptions[subclass.__name__] = {
                "value": {
                    "detail": {"code": subclass.ERROR_CODE, "message": subclass.MESSAGE}
                }
            }
            additional_example = subclass.additional_example()
            if additional_example is not None:
                all_exceptions[subclass.__name__]["value"]["detail"][
                    "additional"
                ] = additional_example

    if len(all_exceptions) == 0:
        raise RuntimeError("No OpenAPI examples found!")
    elif error_codes is not None and len(all_exceptions) != len(error_codes):
        raise RuntimeError(
            'Not all exceptions in "error_codes" could be matched with an error!'
        )
    print(all_exceptions)
    return all_exceptions
