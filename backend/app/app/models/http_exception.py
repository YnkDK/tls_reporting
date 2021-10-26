import pydantic
from pydantic import BaseModel


class ExceptionDetail(BaseModel):
    message: str = pydantic.Field(
        ...,
        title='The error message.',
        description='A human readable english description of why this did happen.',
        example='An error occurred during encoding/decoding the content to/from Gzip.',
    )

    code: str = pydantic.Field(
        ...,
        title='The unique error code.',
        description='Each error has it unique code to identify why this did happen.',
        regex=r'^\d{3}-\d{2}$',
        example='422-01'
    )


class HttpException(BaseModel):
    detail: ExceptionDetail
