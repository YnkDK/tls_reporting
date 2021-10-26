from fastapi import APIRouter

from app.api.api_v1.endpoints import mta_sts_reports

api_v1_router = APIRouter()
api_v1_router.include_router(mta_sts_reports.router, tags=['MTA-STS Reports'])
