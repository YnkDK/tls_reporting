import os
import sys

from app.core import config
from app.core.exceptions import InternalServerError, TLSReportingExceptionBase
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request as StarletteRequest

if not os.path.dirname(os.path.dirname(os.path.realpath(__file__))) in sys.path:
    import warnings

    dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    sys.path.insert(0, dir_path)
    warnings.warn("Missing in sys.path: %s" % dir_path, RuntimeWarning)

from api.api_v1.api import api_v1_router
from fastapi import FastAPI

app = FastAPI(title=config.APPLICATION_NAME, description=config.APPLICATION_DESCRIPTION)

app.include_router(api_v1_router)


@app.exception_handler(StarletteHTTPException)
def http_exception_handler(request: StarletteRequest, exc: StarletteHTTPException):
    if not isinstance(exc, TLSReportingExceptionBase):
        exc = InternalServerError(exc)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
