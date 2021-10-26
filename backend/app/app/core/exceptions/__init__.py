from fastapi import HTTPException, status


class TLSReportingExceptionBase(HTTPException):
    def __init__(self, original_exception: Exception, message: str, error_code: str, http_status_code: int):
        super(TLSReportingExceptionBase, self).__init__(
            status_code=http_status_code,
            detail={
                'message': message,
                'code': error_code
            }
        )
        self.original_exception = original_exception


class GzipError(TLSReportingExceptionBase):
    STATUS_CODE = status.HTTP_422_UNPROCESSABLE_ENTITY
    MESSAGE = 'An error occurred during encoding/decoding the content to/from Gzip.'
    ERROR_CODE = '422-01'

    def __init__(self, original_exception: Exception):
        super(GzipError, self).__init__(
            original_exception=original_exception,
            message=GzipError.MESSAGE,
            error_code=GzipError.ERROR_CODE,
            http_status_code=GzipError.STATUS_CODE
        )


class JsonError(TLSReportingExceptionBase):
    STATUS_CODE = status.HTTP_422_UNPROCESSABLE_ENTITY
    MESSAGE = 'An error occurred while parsing the JSON content, e.g., not well formatted or incorrect types.'
    ERROR_CODE = '422-02'

    def __init__(self, original_exception: Exception):
        super(JsonError, self).__init__(
            original_exception=original_exception,
            message=JsonError.MESSAGE,
            error_code=JsonError.ERROR_CODE,
            http_status_code=JsonError.STATUS_CODE
        )
