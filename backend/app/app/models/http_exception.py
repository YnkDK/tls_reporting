from typing import Optional, List, Any

import pydantic
from pydantic import BaseModel


class ExceptionDetail(BaseModel):
    message: str = pydantic.Field(
        ...,
        title='The error message.',
        description='A human readable english description of why this did happen.'
    )

    code: str = pydantic.Field(
        ...,
        title='The unique error code.',
        description='Each error has it unique code to identify why this did happen.',
        regex=r'^\d{3}-\d{2}$',
    )
    additional: Optional[List[Any]] = pydantic.Field(
        None,
        title='Additional information.',
        description='Any additional information that could help identify the error.'
    )


class HttpException(BaseModel):
    detail: ExceptionDetail
